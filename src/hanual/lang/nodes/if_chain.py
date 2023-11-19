from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

from .base_node import BaseNode
from .else_statement import ElseStatement

if TYPE_CHECKING:
    from typing_extensions import Self

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
        self._statements: List[Union[IfStatement, ElifStatement, ElseStatement]] = []

        self._line_range = line_range
        self._lines = lines

    def add_node(self, node: Union[IfStatement, ElifStatement]) -> Self:
        self._statements.append(node)
        return self

    def add_else(self, node: ElseStatement) -> Self:
        self._statements.append(node)
        return self

    def compile(self) -> None:
        raise NotImplementedError

    @property
    def statements(self) -> List[Union[IfStatement, ElifStatement, ElseStatement]]:
        return self._statements
