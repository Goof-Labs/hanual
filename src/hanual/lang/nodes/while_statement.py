from __future__ import annotations

from typing import TYPE_CHECKING

from bytecode import Label, Instr

from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent
from .base_node import BaseNode

from hanual.util.protocalls import Response

if TYPE_CHECKING:
    from hanual.lang.nodes.block import CodeBlock
    from hanual.lang.nodes.conditions import Condition


class WhileStatement(BaseNode):
    __slots__ = (
        "_while",
        "_body",
        "_lines",
        "_line_range",
    )

    def __init__(self, condition: Condition, body: CodeBlock) -> None:
        self._while: Condition = condition
        self._body: CodeBlock = body

    @property
    def condition(self) -> Condition:
        return self._while

    @property
    def body(self) -> CodeBlock:
        return self._body

    def gen_code(self, intents: Intent, **options) -> GENCODE_RET:
        loop_start = Label()
        loop_end = Label()

        yield Response(loop_start)

        # skip over the loop body if the comparison is false
        yield from self._while.gen_code(self.CAPTURE_RESULT)
        yield Response(Instr("POP_JUMP_IF_FALSE", loop_end))
        # compile the loop body
        yield from self._body.gen_code(self.IGNORE_RESULT)
        # check the condition, jump forward (out the loop) if False, jump backward by default
        yield from self._while.gen_code(self.CAPTURE_RESULT)
        yield Response(Instr("POP_JUMP_IF_FALSE", loop_end))
        yield Response(Instr("JUMP_BACKWARD", loop_start))

        yield Response(loop_end)

    def prepare(self) -> PREPARE_RET:
        yield from self._while.prepare()
        yield from self._body.prepare()
