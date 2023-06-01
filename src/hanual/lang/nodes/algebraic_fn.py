from __future__ import annotations


from .algebraic_expr import AlgebraicExpression
from typing import Any, Dict, TYPE_CHECKING
from .base_node import BaseNode

if TYPE_CHECKING:
    ...


class AlgebraicFunc(BaseNode):
    __slots__ = "_name", "_expr"

    def __init__(self: BaseNode, name: str, expr: AlgebraicExpression) -> None:
        self._name = name
        self._expr = expr

    def as_dict(self) -> Dict[str, Any]:
        return {"name": self._name, "expr": self.get_repr(self._expr)}

    def compile(self, global_state) -> Any:
        raise NotImplementedError
