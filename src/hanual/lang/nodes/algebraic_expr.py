from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from hanual.lang.util.line_range import LineRange


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

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
