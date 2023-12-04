from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    Type,
    Self
)

from hanual.lang.productions import DefaultProduction
from hanual.lang.util.line_range import LineRange

if TYPE_CHECKING:
    from hanual.api.hooks import RuleHook
    from hanual.lang.pparser import _StackFrame

"""
This is a proxy class that wraps around a function, I
was initially adding attributes directly on the
function, but this was a bad idea for several reasons.
This class will store:
 - :production: of the function aka how we would want to access tokens
 - :types: what the function matched with
"""


class Proxy[F: Callable, P:DefaultProduction]:
    __slots__ = "_fn", "_types", "_prod", "_unless_b", "_unless_e"

    def __init__(
            self: Self,
            fn: F,
            types: Dict[str, Any],
            prod: type[P] = DefaultProduction,
            unless_start: Iterable[str] = (),
            unless_end: Iterable[str] = (),
    ) -> None:
        self._fn: F = fn
        self._prod: Type[P] = prod
        self._types = types or {}
        self._unless_b = unless_start or tuple()
        self._unless_e = unless_end or tuple()

    @property
    def prod(self) -> Type[P]:
        return self._prod

    @property
    def types(self) -> Dict[str, Any]:
        return self._types

    @property
    def unless_start(self) -> Iterable[str]:
        return self._unless_b

    @property
    def unless_end(self) -> Iterable[str]:
        return self._unless_e

    @property
    def fn(self) -> F:
        return self._fn

    def call(self: Proxy, args: list[_StackFrame]):
        ln_range = LineRange(-1, -1)
        pattern = []
        values = []
        lines = ""

        for frame in args:  # iterating over raw stack frames passed
            pattern.append(frame.name)
            values.append(frame.value)

            # create a line range to say where code starts and ends
            if ln_range.start == -1:
                ln_range.start = (
                    frame.line_range
                    if isinstance(frame.line_range, int)
                    else frame.line_range.start
                )

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
            if (
                f_end := (
                    frame.line_range
                    if isinstance(frame.line_range, int)
                    else frame.line_range.end
                ) > ln_range.end
            ):
                # checks if the next token has a greater range then ours
                if f_end < ln_range.end:
                    # does not fully overlap, like T2 to T3 in diagram
                    frame_lines = frame.lines.split("\n")

                    for line in frame_lines[: ln_range.end - f_end]:
                        lines = lines + line + "\n"

                else:
                    # aligns nicely like T1 to T2
                    lines += frame.lines

            ln_range.end = (
                frame.line_range
                if isinstance(frame.line_range, int)
                else frame.line_range.end
            )

            # don't want to pass a case

        func_args = self._fn.__annotations__.keys()

        # TODO warn user if lines or line_range is a function argument, now passed through implicitly

        #
        # No types defined
        #
        if self._types != {}:
            try:
                if "lines" in func_args and "line_range" in func_args:
                    res = self._fn(
                        self.prod(values, lines=lines, line_range=ln_range),
                        self.types[" ".join(pattern)],
                        lines=lines,
                        line_range=ln_range,
                    )

                else:
                    res = self._fn(
                        self.prod(values, lines=lines, line_range=ln_range),
                        self.types[" ".join(pattern)],
                        lines=lines,
                        line_range=ln_range,
                    )
                    res.lines = lines
                    res.line_range = ln_range

                return res

            except Exception as e:
                e.add_note(
                    f"{self._fn.__name__!r}@ SIG {list(map(lambda x: x.name, args))!r}"
                )
                raise e

        #
        # Normal execution
        #
        try:
            if "lines" in func_args and "line_range" in func_args:
                res = self._fn(self.prod(values, lines=lines, line_range=ln_range))

            else:
                res = self._fn(self.prod(values))
                res.lines = lines
                res.line_range = ln_range

        except Exception as e:
            e.add_note(
                f"{self._fn.__name__!r} @ SIG {list(map(lambda x: x.name, args))!r}"
            )
            raise e

        return res


class HookProxy[P](Proxy):
    def __init__(
            self,
            cls: Type[RuleHook],
            types: Dict[str, Any],
            prod: type[P] = DefaultProduction,
            unless_start: Iterable[str] = (),
            unless_end: Iterable[str] = (),
    ) -> None:
        super().__init__(cls(), types, prod, unless_start, unless_end)

    def call(self: Proxy, args):
        raise NotImplementedError
