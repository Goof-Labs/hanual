from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.algebraic_expr import AlgebraicExpression
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class AlgebraicFunc(BaseNode):
    __slots__ = (
        "_name",
        "_expr",
        "_lines",
        "_line_range",
    )

    def __init__(
        self, name: str, expr: AlgebraicExpression, lines: str, line_range: LineRange
    ) -> None:
        self._name = name
        self._expr = expr

        self._lines = lines
        self._line_range = line_range

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        raise NotImplementedError
