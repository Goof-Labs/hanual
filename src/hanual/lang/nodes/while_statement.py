from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.compile.constants.constant import Constant
from hanual.compile.instruction import *
from hanual.compile.label import Label

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.nodes.block import CodeBlock
    from hanual.lang.nodes.conditions import Condition


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

    def compile(self):
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
