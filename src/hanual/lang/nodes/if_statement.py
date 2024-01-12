from __future__ import annotations

from typing import TYPE_CHECKING

from bytecode import Instr, Label

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.util import Response

if TYPE_CHECKING:
    from .block import CodeBlock
    from .conditions import Condition


class IfStatement(BaseNode):
    __slots__ = "_condition", "_block", "_lines", "_line_range"

    def __init__(self, condition: Condition, block: CodeBlock) -> None:
        self._condition: Condition = condition
        self._block: CodeBlock = block

    @property
    def condition(self) -> Condition:
        return self._condition

    @property
    def block(self) -> CodeBlock:
        return self._block

    def gen_code(self) -> GENCODE_RET:
        false_jump = Label()

        yield from self._condition.gen_code()
        yield Response[Instr](
            Instr("POP_JUMP_IF_FALSE", false_jump, location=self.get_location())
        )

        yield from self._block.gen_code()

        yield Response[Label](false_jump)

    def prepare(self) -> PREPARE_RET:
        yield from self._condition.prepare()
        yield from self._block.prepare()
