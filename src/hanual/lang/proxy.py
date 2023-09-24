from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, Optional, Type, Union, List

from .productions import DefaultProduction, P
from .util.line_range import LineRange

if TYPE_CHECKING:
    from typing_extensions import Self
    from .pparser import _StackFrame

    from hanual.api.hooks import RuleHook

"""
This is a proxy class that wraps around a function, I
was initially adding attributes directly on the
function, but this was a bad idea for several reasons.
This class will store:
 - :production: of the function aka how we would want to access tokens
 - :types: what the function matched with
"""


class Proxy:
    __slots__ = "_fn", "_types", "_prod", "_unless_b", "_unless_e"

    def __init__(
        self: Self,
        fn: Union[Callable[[P], Any], Callable[[P, Optional[Dict]], Any], RuleHook],
        types: Dict[str, Any],
        prod: type[P] = None,
        unless_start: Iterable[str] = (),
        unless_end: Iterable[str] = (),
    ) -> None:
        self._fn: Union[
            Callable[[P], Any], Callable[[P, Optional[Dict]], Any], RuleHook
        ] = fn
        self._prod: Type[P] = prod or DefaultProduction
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
    def fn(self) -> Union[Callable[[P], Any], Callable[[P, Optional[Dict]], Any]]:
        return self._fn

    def call(self: Proxy, args: List[_StackFrame]):
        ln_range = LineRange(-1, -1)
        pattern = []
        values = []
        lines = ""

        for frame in args:  # iterating over raw stack frames passed
            pattern.append(frame.name)
            values.append(frame.value)

            # create a line range to say where code starts and ends
            if ln_range.start == -1:
                ln_range.start = frame.line_no

            ln_range.end = frame.line_no

            lines += frame.lines

        # don't want to pass a case
        if self._types != {}:
            return self._fn(self.prod(values, lines=lines, line_no=ln_range), pattern, lines=lines, line_no=ln_range)

        return self._fn(self.prod(values, lines=lines, line_no=ln_range), lines=lines, line_no=ln_range)


class HookProxy(Proxy):
    def __init__(
        self,
        cls: Type[RuleHook],
        types: Dict[str, Any],
        prod: type[P] = None,
        unless_start: Iterable[str] = (),
        unless_end: Iterable[str] = (),
    ) -> None:
        super().__init__(cls(), types, prod, unless_start, unless_end)

    def call(self: Proxy, args):
        raise NotImplementedError
