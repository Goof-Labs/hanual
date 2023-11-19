from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack
from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    from .f_call import FunctionCall


class ImplicitBinOp(BaseNode):
    __slots__ = ("_right", "_op", "_lines", "_line_range")

    def __init__(
        self, op: Token, right: Union[Token, FunctionCall], lines: str, line_range: int
    ) -> None:
        # The left side is implied
        self._right = right
        self._op = op

        self._line_range = line_range
        self._lines = lines

    @property
    def op(self) -> Token:
        return self._op

    @property
    def right(self) -> Union[Token, FunctionCall]:
        return self._right

    def compile(self):
        raise NotImplementedError
