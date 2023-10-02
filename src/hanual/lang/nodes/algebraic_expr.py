from __future__ import annotations

from abc import ABC
from typing import Union

from hanual.lang.lexer import Token

from .base_node import BaseNode


class AlgebraicExpression(BaseNode, ABC):
    __slots__ = "_op", "_left", "_right", "_lines", "_line_no",

    def __init__(
        self: BaseNode,
        operator: Token,
        left: Union[AlgebraicExpression, Token],
        right: Union[AlgebraicExpression, Token],
        lines: str,
        line_no: int
    ) -> None:
        self._op = operator
        self._left = left
        self._right = right

        self._lines = lines
        self._line_no = line_no

    def compile(self) -> None:
        raise NotImplementedError
