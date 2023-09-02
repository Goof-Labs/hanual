from __future__ import annotations

from hanual.compile.constants.constant import Constant
from typing import TYPE_CHECKING, List, Union
from .else_statement import ElseStatement
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self
    from .elif_statement import ElifStatement
    from .if_statement import IfStatement


class IfChain(BaseNode):
    __slots__ = "_statements",

    def __init__(self) -> None:
        self._statements: List[Union[IfStatement, ElifStatement, ElseStatement]] = []

    def add_node(self, node: Union[IfStatement, ElifStatement]) -> Self:
        self._statements.append(node)
        return self

    def add_else(self, node: ElseStatement) -> Self:
        self._statements.append(node)
        return self

    def compile(self) -> None:
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

    def execute(self, scope: Scope):
        res = Result()

        for statement in self._statements:
            # check if one of the conditions was true, if so we just return the result
            ran, err = res.inherit_from(statement.execute(scope=scope))

            if err:
                return res

            # if a statement was run, just return it
            if ran:
                return res

            # if the statement is an "else", we want to execute it regardless.
            if isinstance(statement, ElseStatement):
                return statement.execute(scope)

        # the entire chain was run and none of them where true
        return res.success(None)

    def find_priority(self) -> list[BaseNode]:
        return []

    @property
    def statements(self) -> List[Union[IfStatement, ElifStatement, ElseStatement]]:
        return self._statements
