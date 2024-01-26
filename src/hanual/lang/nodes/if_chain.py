from __future__ import annotations

from typing import TYPE_CHECKING, Self

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.else_statement import ElseStatement
from hanual.util.protocalls import Response
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent
from .elif_statement import ElifStatement
from .if_statement import IfStatement
from bytecode import Label

if TYPE_CHECKING:
    ...



class IfChain(BaseNode):
    __slots__ = (
        "_statements",
        "_lines",
        "_line_range",
    )

    def __init__(self) -> None:
        self._statements: list[IfStatement | ElifStatement | ElseStatement] = []

    def add_node(self, node: IfStatement | ElifStatement) -> Self:
        assert isinstance(node, (IfStatement, ElifStatement))
        self._statements.append(node)
        return self

    def add_else(self, node: ElseStatement) -> Self:
        self._statements.append(node)
        return self

    @property
    def statements(self) -> list[IfStatement | ElifStatement | ElseStatement]:
        return self._statements

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        true_jump = Label()

        for stmt in self.statements:
            if isinstance(stmt, (IfStatement, ElifStatement)):
                yield from stmt.gen_code(true_jump=true_jump)

            else:
                assert isinstance(stmt, ElseStatement), f"Last statement must be an else go a {stmt}"
                yield from stmt.gen_code()

        yield Response(true_jump)


    def prepare(self) -> PREPARE_RET:
        for statement in self._statements:
            yield from statement.prepare()
