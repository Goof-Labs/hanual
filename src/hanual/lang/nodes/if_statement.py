from __future__ import annotations

from hanual.compile.instruction import InstructionJEZ
from typing import Any, TYPE_CHECKING
from .base_node import BaseNode
from .block import CodeBlock
from abc import ABC


if TYPE_CHECKING:
    from .conditions import Condition
    from hanual.compile import Assembler


class IfStatement(BaseNode, ABC):
    def __init__(self: IfStatement, condition: Condition, if_true: CodeBlock) -> None:
        self._condition = condition
        self._iftrue = if_true

    def compile(self, global_state: Assembler) -> Any:
        # evaluate condition
        self._condition.compile(global_state)

        jmp_false_label = global_state.add_label(
            name="if", add_now=False
        )  # push on later
        global_state.add_instructions(InstructionJEZ(jmp_false_label.idx))

        # dump the body of the if code
        self._iftrue.compile(global_state)

        global_state.add_label(jmp_false_label)
