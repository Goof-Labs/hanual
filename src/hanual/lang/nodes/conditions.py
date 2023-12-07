from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.util import Reply, Response, Request

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.lexer import Token

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class Condition[L: (Token, BaseNode), R: (Token, BaseNode)](BaseNode):
    __slots__ = "_op", "_left", "_right", "_lines", "_line_range"

    def __init__(self, op: Token, left, right, lines: str, line_range: LineRange) -> None:
        self._right: R = right
        self._left: L = left
        self._op: Token = op

        self._line_range = line_range
        self._lines = lines

    @property
    def op(self) -> Token:
        return self._op

    @property
    def left(self) -> L:
        return self._left

    @property
    def right(self) -> R:
        return self._right

    def compile(self) -> Generator[Reply | Request, Response, None]:
        raise NotImplementedError
