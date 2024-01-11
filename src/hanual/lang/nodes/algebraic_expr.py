from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Optional

from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Response, Request, REQUEST_TYPE

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from hanual.lang.lexer import Token


class AlgebraicExpression(BaseNode):
    __slots__ = (
        "_op",
        "_left",
        "_right",
        "_lines",
        "_line_range",
    )

    def __init__(
        self,
        operator: Token,
        left: AlgebraicExpression | Token,
        right: AlgebraicExpression | Token,
        lines: str,
        line_range: LineRange,
    ) -> None:
        self._op: Token = operator
        self._left = left
        self._right = right

        self._lines = lines
        self._line_range = line_range

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
