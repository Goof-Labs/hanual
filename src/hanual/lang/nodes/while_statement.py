from __future__ import annotations

from hanual.compile.constant import Constant
from hanual.lang.nodes.base_node import BaseNode
from typing import Any, Dict, TYPE_CHECKING
from hanual.compile.instruction import *
from hanual.compile.label import Label

if TYPE_CHECKING:
    from hanual.lang.nodes.conditions import Condition
    from hanual.lang.nodes.block import CodeBlock


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

    def compile(self) -> None:
        instructions = []

        while_start = Label("WHILE", mangle=True)

        instructions.append(while_start)
        instructions.extend(self._while.compile())
        instructions.extend(self.body.compile())
        instructions.append(JIT(while_start))

        return instructions

    def execute(self):
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        return [*self._while.get_constants(), *self._body.get_constants()]

    def get_names(self) -> list[str]:
        return [*self._while.get_names(), *self._body.get_names()]

    def find_priority(self) -> list[BaseNode]:
        return self._body.find_priority()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "condition": self._while.as_dict()
            if hasattr(self._while, "as_dict")
            else self._while,
            "inner": self._body.as_dict()
            if hasattr(self._body, "as_dict")
            else self._body,
        }
