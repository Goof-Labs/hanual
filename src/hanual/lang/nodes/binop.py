from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class BinOpNode[L: (Token, BaseNode), R: (Token, BaseNode)](BaseNode):
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

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
