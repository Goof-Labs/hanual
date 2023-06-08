from __future__ import annotations


from hanual.runtime import RuntimeEnvironment, ExecStatus
from typing import Any, Dict, Union, List, TYPE_CHECKING
from hanual.lang.errors import Error
from .base_node import BaseNode


if TYPE_CHECKING:
    from .elif_statement import ElifStatement
    from .else_statement import ElseStatement
    from .if_statement import IfStatement


class IfChain(BaseNode):
    def __init__(self: BaseNode) -> None:
        self._statements: List[Union[IfStatement, ElifStatement, ElseStatement]] = []

    def add_node(self, node: Union[IfStatement, ElifStatement]) -> Self:
        self._statements.append(node)
        return self

    def add_else(self, node: ElseStatement) -> Self:
        self._statements.append(node)
        return self

    def compile(self, ir) -> None:
        raise NotImplementedError

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        for statement in self._statements:
            err, res = sts = statement.execute(rte)

            if err:
                return sts

    @property
    def statements(self) -> List[Union[IfStatement, ElifStatement, ElseStatement]]:
        return self._statements

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
