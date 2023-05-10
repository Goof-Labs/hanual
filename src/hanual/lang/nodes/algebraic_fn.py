from __future__ import annotations

from .algebraic_expr import AlgebraicExpression
from .base_node import BaseNode


class AlgebraicFunc(BaseNode):
    __slots__ = "_name", "_expr"

    def __init__(self: BaseNode, name: str, expr: AlgebraicExpression) -> None:
        self._name = name
        self._expr = expr
