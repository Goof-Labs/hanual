from __future__ import annotations

from typing import Any, Callable, Dict, Optional, Iterable, Type, Union, TYPE_CHECKING
from .productions import DefaultProduction, P

if TYPE_CHECKING:
    from hanual.api.hook import RuleHook
    from typing_extensions import Self

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
        self._fn: Union[Callable[[P], Any], Callable[[P, Optional[Dict]], Any], RuleHook] = fn
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

    def call(self: Proxy, args, pattern):
        # don't want to pass a case
        if self._types != {}:
            return self._fn(self.prod(args), self.types.get(" ".join(pattern), None))

        return self._fn(self.prod(args))


class HookProxy(Proxy):
    def __init__(self,
                 cls: Type[RuleHook], types: Dict[str, Any],
                 prod: type[P] = None,
                 unless_start: Iterable[str] = (),
                 unless_end: Iterable[str] = ()) -> None:
        super().__init__(cls(), types, prod, unless_start, unless_end)

    def call(self: Proxy, args, pattern):
        # don't want to pass a case
        assert hasattr(self._fn, "create_rule"),\
            TypeError(f"Must be RuleHook to use HookProxy, got {type(self._fn).__name__!r}")

        if self._types != {}:
            return self._fn.create_rule(self.prod(args), self.types.get(" ".join(pattern), None))

        return self._fn.create_rule(self.prod(args))
