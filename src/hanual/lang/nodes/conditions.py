from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Union

from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class Condition(BaseNode, ABC):
    __slots__ = "_op", "_left", "_right", "_lines", "_line_range"

    def __init__(
        self: BaseNode, op: Token, left, right, lines: str, line_range: LineRange
    ) -> None:
        self._right: Union[Token, BaseNode] = right
        self._left: Union[Token, BaseNode] = left
        self._op: Token = op

        self._line_range = line_range
        self._lines = lines

    @property
    def op(self):
        return self._op

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def compile(self):
        raise NotImplementedError
