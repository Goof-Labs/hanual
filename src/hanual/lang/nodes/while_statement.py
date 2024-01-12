from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.nodes.block import CodeBlock
    from hanual.lang.nodes.conditions import Condition
    from hanual.lang.util.line_range import LineRange


class WhileStatement(BaseNode):
    __slots__ = (
        "_while",
        "_body",
        "_lines",
        "_line_no",
    )

    def __init__(
        self, condition: Condition, body: CodeBlock, lines: str, line_no: LineRange
    ) -> None:
        self._while: Condition = condition
        self._body: CodeBlock = body

        self._line_no = line_no
        self._lines = lines

    @property
    def condition(self) -> Condition:
        return self._while

    @property
    def body(self) -> CodeBlock:
        return self._body

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
