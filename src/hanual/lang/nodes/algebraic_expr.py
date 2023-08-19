from __future__ import annotations

from abc import ABC
from typing import Union

from hanual.lang.lexer import Token

from .base_node import BaseNode


class AlgebraicExpression(BaseNode, ABC):
    __slots__ = "_op", "_left", "_right"

    def __init__(
        self: BaseNode,
        operator: Token,
        left: Union[AlgebraicExpression, Token],
        right: Union[AlgebraicExpression, Token],
    ) -> None:
        self._op = operator
        self._left = left
        self._right = right

    def compile(self) -> None:
        raise NotImplementedError
