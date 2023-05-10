from __future__ import annotations

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.lexer import Token
from .base_node import BaseNode
from typing import Union


class AlgebraicExpression(BaseNode):
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
