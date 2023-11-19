from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Union

from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack
from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    ...


class BinOpNode(BaseNode, ABC):
    __slots__ = "_right", "_left", "_op", "_lines", "_line_range"

    def __init__(self, op: Token, left, right, lines: str, line_range: int) -> None:
        self._right: Union[Token, BinOpNode] = right
        self._left: Union[Token, BinOpNode] = left

        self._op: Token = op

        self._lines = lines
        self._line_range = line_range

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def op(self):
        return self._op

    def compile(self):
        raise NotImplementedError
