from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class BinOpNode[L: (Token, BaseNode), R: (Token, BaseNode)](BaseNode, ABC):
    __slots__ = "_right", "_left", "_op", "_lines", "_line_range"

    def __init__(
            self,
            op: Token,
            left: L,
            right: R,
            lines: str,
            line_range: LineRange,
    ) -> None:
        self._right: R = right
        self._left: L = left

        self._op: Token = op

        self._lines = lines
        self._line_range = line_range

    @property
    def left(self) -> L:
        return self._left

    @property
    def right(self) -> R:
        return self._right

    @property
    def op(self) -> Token:
        return self._op

    def compile(self):
        raise NotImplementedError
