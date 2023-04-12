from __future__ import annotations

from .productions import DefaultProduction, PInterface
from typing import Self, Callable, Any, Dict

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
        fn: Callable[[Any], Any],
        types: Dict[str, Any],
        prod: PInterface = None,
    ) -> None:
        self._prod: PInterface = prod or DefaultProduction
        self._types = types or {}
        self._fn = fn

    @property
    def prod(self) -> PInterface:
        return self._prod

    @property
    def types(self) -> Dict[str, Any]:
        return self._types

    @property
    def fn(self) -> Callable[[Any], Any]:
        return self._fn

    def call(self: Proxy, args, pattern):
        return self._fn(self.prod(args), case=self.types.get(" ".join(pattern), None))
