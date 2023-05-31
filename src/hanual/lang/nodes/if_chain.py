from __future__ import annotations


from typing import Any, Dict, Union, List, TYPE_CHECKING
from typing_extensions import Self
from hanual.compile.ir import IR
from .base_node import BaseNode


if TYPE_CHECKING:
    from .elif_statement import ElifStatement
    from .else_statement import ElseStatement
    from .if_statement import IfStatement


class IfChain(BaseNode):
    def __init__(self: BaseNode) -> None:
        self._statements = []

    @property
    def statements(self) -> List[Union[IfStatement, ElifStatement, ElseStatement]]:
        return self._statements

    def add_node(self, node: Union[IfStatement, ElifStatement]) -> Self:
        self._statements.append(node)
        return self

    def add_else(self, node: ElseStatement) -> Self:
        self._statements.append(node)
        return self

    def compile(self, ir: IR, to: str | None) -> None:
        return super().compile(ir, to)

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
