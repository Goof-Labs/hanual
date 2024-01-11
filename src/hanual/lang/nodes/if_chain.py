from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Self, Optional

from .base_node import BaseNode
from .else_statement import ElseStatement

from hanual.util import Reply, Request, Response, REQUEST_TYPE


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

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
