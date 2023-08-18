from __future__ import annotations

from .algebraic_expr import AlgebraicExpression
from typing import Any, TYPE_CHECKING
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    ...


class AlgebraicFunc(BaseNode, ABC):
    __slots__ = "_name", "_expr"

    def __init__(self: BaseNode, name: str, expr: AlgebraicExpression) -> None:
        self._name = name
        self._expr = expr

    def compile(self) -> Any:
        raise NotImplementedError
