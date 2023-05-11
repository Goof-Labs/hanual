from __future__ import annotations
from typing import Any, Dict

from hanual.compile import Assembler

from .algebraic_expr import AlgebraicExpression
from .base_node import BaseNode


class AlgebraicFunc(BaseNode):
    __slots__ = "_name", "_expr"

    def __init__(self: BaseNode, name: str, expr: AlgebraicExpression) -> None:
        self._name = name
        self._expr = expr

    def as_dict(self) -> Dict[str, Any]:
        return {"name": self._name, "expr": self.get_repr(self._expr)}

    def compile(self, global_state: Assembler) -> Any:
        return super().compile(global_state)
