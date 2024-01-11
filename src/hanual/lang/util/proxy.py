from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Type, Self

from hanual.lang.util.compileable_object import CompilableObject
from hanual.lang.productions import DefaultProduction
from hanual.lang.util.line_range import LineRange


if TYPE_CHECKING:
    from hanual.lang.pparser import _StackFrame
    from hanual.api.hooks import RuleHook

"""
This is a proxy class that wraps around a function, I
was initially adding attributes directly on the
function, but this was a bad idea for several reasons.
This class will store:
 - :production: of the function aka how we would want to access tokens
 - :types: what the function matched with
"""


class Proxy[F: Callable]:
    __slots__ = "_fn", "_types", "_prod", "_unless_b", "_unless_e"

    def __init__(
        self: Self,
        fn: F,
        types: dict[str, Any] | None = None,
        prod: Type | None = None,
        unless_start: list[str] | None = None,
        unless_end: list[str] | None = None,
    ) -> None:
        self._fn: F = fn
        self._prod: Type = prod or DefaultProduction
        self._types = types or {}
        self._unless_b = unless_start or []
        self._unless_e = unless_end or []

    @property
    def prod(self) -> Type:
        return self._prod

    @property
    def types(self) -> dict[str, Any]:
        return self._types

    @property
    def unless_start(self) -> list[str]:
        return self._unless_b

    @property
    def unless_end(self) -> list[str]:
        return self._unless_e

    @property
    def fn(self) -> F:
        return self._fn

    def call(self: Proxy, args: list[_StackFrame]) -> CompilableObject:
        ln_range = LineRange(start=float("inf"), end=float("-inf"))
        pattern = []
        values = []
        lines = ""

        for frame in args:  # iterating over raw stack frames passed
            pattern.append(frame.name)
            values.append(frame.value)

            # create a line range to say where code starts and ends
            ln_range_end = frame.value.line_range.end
            ln_range_start = frame.value.line_range.start

            if ln_range.start > ln_range_start:
                ln_range.start = ln_range_start

            """
            The problem is that some lines will just overlap. Tokens will store the line they are from and
            this can be used to construct the environment they where made in. But we may have three tokens
            NUM(line="1+2") PLUS(line="1+2") NUM(line="1+2")
            In this scenario a bare implementation might just use a string and concatenate all strings
            together this has the slight downside of lines being duplicated, in the above example the result
            would be
            1+21+21+2
            Which is far from accurate. A better implementation may save the last line and check if the
            current one is identical. This would work in the example, but if the programmer intentionally
            writes two identical statements, parts of the code may be omitted.
            The best solution is to use the hl_range variable and see if the current lines are in range
            if they are in the range then we have probably covered them and should move on, else just add
            them.
            NUM(line="1+2", start=0, end=0) PLUS(line="1+2", start=0, end=1) NUM(line="1+2", start=0, end=1)
            This time only the first line should be included because all the others have the same range,
            with an improved implementation parts of the lines can be spliced.
            T1 = |------|
            T2 =        |------|
            T3 =            |------|
            The above is a diagram that would show the splicing in action.
            """
            if ln_range_end > ln_range.end:
                # checks if the next token has a greater range then ours
                if ln_range_end < ln_range.end:
                    # does not fully overlap, like T2 to T3 in diagram
                    frame_lines = frame.lines.split("\n")

                    for line in frame_lines[: ln_range.end - ln_range_end]:
                        lines = lines + line + "\n"

                else:
                    # aligns nicely like T1 to T2
                    lines += frame.lines

            ln_range.end = ln_range_end

        if not ln_range.end >= 1:
            ln_range.end = ln_range.start

        func_args = self._fn.__annotations__.keys()

        # TODO warn user if lines or line_range is a function argument, now passed through implicitly

        #
        # Types defined
        #
        if self._types != {}:
            try:
                if "lines" in func_args and "line_range" in func_args:
                    res = self._fn(
                        self.prod(values),
                        self.types.get(" ".join(pattern), None) or self.types.get("*"),
                        lines=lines,
                        line_range=ln_range,
                    )

                else:
                    res = self._fn(
                        self.prod(values),
                        self.types.get(" ".join(pattern), None) or self.types.get("*"),
                    )
                    res.lines = lines
                    res.line_range = ln_range

                return res

            except ExceptionGroup as e:
                e.add_note(
                    f"@rule{tuple(map(lambda x: x.name, args))!r}\ndef {self._fn.__name__} ..."
                )
                raise e

        #
        # No types defined
        #
        try:
            if "lines" in func_args and "line_range" in func_args:
                res = self._fn(self.prod(values))

            else:
                # should be using this vv
                res = self._fn(self.prod(values))
                res.lines = lines
                res.line_range = ln_range

        except Exception as e:
            e.add_note(f"@rule{tuple(map(lambda x: x.name, args))!r}\n")
            raise e

        return res


class HookProxy(Proxy):
    def __init__(
        self,
        cls: Type[RuleHook],
        types: dict[str, Any] | None = None,
        prod: type | None = None,
        unless_start: list[str] | None = None,
        unless_end: list[str] | None = None,
    ):
        raise NotImplementedError

    def call(self: Proxy, args):
        raise NotImplementedError
