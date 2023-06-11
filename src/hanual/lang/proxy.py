from __future__ import annotations

from typing import Callable, Any, Dict, Type, Union, Sequence, Optional
from .productions import DefaultProduction, P

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
        fn: Union[Callable[[P], Any], Callable[[P, Optional[Dict]], Any]],
        types: Dict[str, Any],
        prod: type[P] = None,
        unless_start: Sequence[str] = (),
        unless_end: Sequence[str] = (),
    ) -> None:
        self._fn: Union[Callable[[P], Any], Callable[[P, Optional[Dict]], Any]] = fn
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
    def unless_start(self) -> Sequence[str]:
        return self._unless_b

    @property
    def unless_end(self) -> Sequence[str]:
        return self._unless_e

    @property
    def fn(self) -> Union[Callable[[P], Any], Callable[[P, Optional[Dict]], Any]]:
        return self._fn

    def call(self: Proxy, args, pattern):
        # don't want to pass case
        if self._types != {}:
            return self._fn(self.prod(args), self.types.get(" ".join(pattern), None))

        return self._fn(self.prod(args))
