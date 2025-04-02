from __future__ import annotations

from typing import TYPE_CHECKING

from bytecode import Instr, Label

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_compile_options import IF_STATEMENT_KWARGS
from hanual.util.equal_list import ItemEqualList
from hanual.lang.util.node_utils import Intent
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

    def gen_code(self,
                 intents: ItemEqualList[Intent],
                 **options: IF_STATEMENT_KWARGS) -> GENCODE_RET:

        if (fj := options.get("end_jump", None)) is not None:
            false_jump = fj

        else:
            false_jump = Label()

        yield from self._condition.gen_code()
        yield Response[Instr](
            Instr("POP_JUMP_IF_FALSE", false_jump, location=self.get_location())
        )

        yield from self._block.gen_code()

        # if the if is part of a chain, we want to jump to the end of the chain.
        true_jump = options.get("true_jump")

        if true_jump:
            yield Response(Instr("JUMP_FORWARD", true_jump))

        yield Response(false_jump)

    def prepare(self) -> PREPARE_RET:
        yield from self._condition.prepare()
        yield from self._block.prepare()
