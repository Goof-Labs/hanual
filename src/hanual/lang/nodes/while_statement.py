from __future__ import annotations


from hanual.compile import Assembler
from hanual.lang.nodes.conditions import Condition
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.block import CodeBlock
from typing import Any, Dict


class WhileStatement(BaseNode):
    def __init__(self: BaseNode, condition: Condition, body: CodeBlock) -> None:
        self._whle: Condition = condition
        self._body: CodeBlock = body

    def as_dict(self) -> Dict[str, Any]:
        return {
            "condition": self._whle.as_dict(),
            "inner": self._body.as_dict(),
        }

    def compile(self, global_state: Assembler) -> Any:
        return super().compile(global_state)
