from __future__ import annotations

from hanual.lang.lexer import Token
from typing import TYPE_CHECKING
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class SGetattr[L: BaseNode, R: Token](BaseNode):
    __slots__ = (
        "_left",
        "_right",
        "_lines",
        "_line_range",
    )

    def __init__(self, left: L, right: R, lines: str, line_range: LineRange) -> None:
        self._left: R = right
        self._right: L = left

        self._line_range = line_range
        self._lines = lines

    def compile(self):
        raise NotImplementedError
