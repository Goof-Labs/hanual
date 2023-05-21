from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
from hanual.lang.nodes.base_node import BaseNode
from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from hanual.lang.nodes.conditions import Condition
    from hanual.lang.nodes.block import CodeBlock
    from hanual.compile import Assembler


class WhileStatement(BaseNode):
    def __init__(self: BaseNode, condition: Condition, body: CodeBlock) -> None:
        self._while: Condition = condition
        self._body: CodeBlock = body

    @property
    def condition(self) -> Condition:
        return self._while

    @property
    def body(self) -> CodeBlock:
        return self._body

    def as_dict(self) -> Dict[str, Any]:
        return {
            "condition": self._while.as_dict()
            if hasattr(self._while, "as_dict")
            else self._while,
            "inner": self._body.as_dict()
            if hasattr(self._body, "as_dict")
            else self._body,
        }

    def compile(self, global_state: Assembler) -> Any:
        while_start = global_state.add_label("while_loop")

        self._body.compile(global_state)
        self._while.compile(global_state)  # push a true or false to stack
        global_state.add_instructions(
            Instruction(InstructionEnum.JEZ, while_start.idx)
        )  # if the while is true we jump
