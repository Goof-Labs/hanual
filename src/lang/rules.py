from __future__ import annotations

from productions import DefaultProduction
from typing import Self, Dict, Any
from pparser import PParser
from proxy import Proxy


class Rules:
    def rule(*args, **kwargs):
        def wrapper(self: Rules, fn):
            prox: Proxy = Proxy(
                fn,
                kwargs.get("types", {}),
                kwargs.get("prod", DefaultProduction),
            )

            for r in args:
                self.parser.rules[r] = prox

        return wrapper

    def __init__(self: Self, parser: PParser) -> None:
        self.parser: PParser = parser
