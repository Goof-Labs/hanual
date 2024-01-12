from __future__ import annotations

from typing import TYPE_CHECKING, Self

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.else_statement import ElseStatement
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange

    from .elif_statement import ElifStatement
    from .if_statement import IfStatement


class IfChain(BaseNode):
    __slots__ = (
        "_statements",
        "_lines",
        "_line_range",
    )

    def __init__(self, lines: str, line_range: LineRange) -> None:
        self._statements: list[IfStatement | ElifStatement | ElseStatement] = []

        self._line_range = line_range
        self._lines = lines

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

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
