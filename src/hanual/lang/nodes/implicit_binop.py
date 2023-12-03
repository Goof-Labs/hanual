from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    from .f_call import FunctionCall


class ImplicitBinOp[O: Token, R: (Token, FunctionCall)](BaseNode):
    __slots__ = ("_right", "_op", "_lines", "_line_range")

    def __init__(self, op: O, right: R, lines: str, line_range: int) -> None:
        # The left side is implied
        self._right = right
        self._op = op

        self._line_range = line_range
        self._lines = lines

    @property
    def op(self) -> O:
        return self._op

    @property
    def right(self) -> R:
        return self._right

    def compile(self):
        raise NotImplementedError
