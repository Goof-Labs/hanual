from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.lexer import Token, Generator
from hanual.lang.nodes.base_node import BaseNode

from hanual.util import Reply, Response, Request


if TYPE_CHECKING:
    from hanual.lang.nodes.f_call import FunctionCall
    from hanual.lang.util.line_range import LineRange


class ImplicitBinOp[O: Token, R: (Token, FunctionCall)](BaseNode):
    __slots__ = ("_right", "_op", "_lines", "_line_range")

    def __init__(self, op: O, right: R, lines: str, line_range: LineRange) -> None:
        # The left side is implied
        self._right = right
        self._op = op

        self._lines = lines
        self._line_range = line_range

    @property
    def op(self) -> O:
        return self._op

    @property
    def right(self) -> R:
        return self._right

    def compile(self) -> Generator[Reply | Request, Response, None]:
        raise NotImplementedError
