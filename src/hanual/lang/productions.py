from __future__ import annotations

from typing import TYPE_CHECKING, List, Self

if TYPE_CHECKING:
    from hanual.lang.nodes.base_node import BaseNode
    from hanual.lang.lexer import Token


class DefaultProduction[T: Token | BaseNode]:
    __slots__ = ("ts", "lines", "line_no")

    def __init__(self: Self, ts: List[T], lines: str, line_range: str) -> None:
        self.ts: List[T] = ts

        self.lines = lines
        self.line_range = line_range

    def __repr__(self: Self) -> str:
        return str(self.ts)

    def __getitem__(self: Self, item: int) -> T:
        return self.ts[item]
