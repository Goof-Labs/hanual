from __future__ import annotations

from typing import Self, Callable, Any, Dict, Type, Union
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
    __slots__ = "_fn", "_types", "_prod"

    def __init__(
        self: Self,
        fn: Union[Callable[[P], Any], Callable[[P, ...], Any]],
        types: Dict[str, Any],
        prod: type[P] = None,
    ) -> None:
        self._prod: Type[P] = prod or DefaultProduction
        self._types = types or {}
        self._fn: Union[Callable[[P], Any], Callable[[P, ...], Any]] = fn

    @property
    def prod(self) -> Type[P]:
        return self._prod

    @property
    def types(self) -> Dict[str, Any]:
        return self._types

    @property
    def fn(self) -> Union[Callable[[P], Any], Callable[[P, ...], Any]]:
        return self._fn

    def call(self: Proxy, args, pattern):
        # don't want to pass case
        if self._types != {}:
            return self._fn(self.prod(args), self.types.get(" ".join(pattern), None))

        return self._fn(self.prod(args))
