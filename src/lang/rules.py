from __future__ import annotations

from pparser import PParser
from typing import Self


class Rules:
    def rule(*args, **kwargs):
        conf = {}

        def wrapper(self: Rules, fn):
            fn._conf = conf

            for r in args:
                self.parser.rules[r] = fn

        return wrapper

    @rule(1, 2, 3, 4, 5, 6, 7, 8, 9)
    def some_rule(self):
        ...

    def __init__(self: Self, parser: PParser) -> None:
        self.parser: PParser = parser
