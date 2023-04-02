from __future__ import annotations

from .productions import DefaultProduction
from .pparser import PParser
from .proxy import Proxy
from typing import Self


class Rules:
    def rule(*args, **kwargs):
        def wrapper(self: Rules, fn):
            prox: Proxy = Proxy(
                fn,
                kwargs.get("types", {}),
                kwargs.get("prod", DefaultProduction),
            )

            for r in args:
                self.parser.rules[r] = fn.__name__, prox

        return wrapper

    def __init__(self: Self, parser: PParser) -> None:
        self.parser: PParser = parser
