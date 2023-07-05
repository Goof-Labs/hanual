from __future__ import annotations
from hanual.compile.constant import Constant


from typing import Any, Dict, Union, List, TYPE_CHECKING
from hanual.lang.errors import Error
from .base_node import BaseNode


if TYPE_CHECKING:
    from .elif_statement import ElifStatement
    from .if_statement import IfStatement
    from typing_extensions import Self


class IfChain(BaseNode):
    def __init__(self: BaseNode) -> None:
        self._statements: List[Union[IfStatement, ElifStatement]] = []

    def add_node(self, node: Union[IfStatement, ElifStatement]) -> Self:
        self._statements.append(node)
        return self

    def add_else(self, node: ElseStatement) -> Self:
        self._statements.append(node)
        return self

    def compile(self, ir) -> None:
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        consts = []

        for stmt in self._statements:
            consts.extend(stmt.get_constants())

        return consts

    def get_names(self) -> list[str]:
        names = []

        for stmt in self._statements:
            names.extend(stmt.get_names())

        return names

    def execute(self):
        for statement in self._statements:
            err, res = sts = statement.execute(rte)

            if err:
                return sts

    @property
    def statements(self) -> List[Union[IfStatement, ElifStatement, ElseStatement]]:
        return self._statements
