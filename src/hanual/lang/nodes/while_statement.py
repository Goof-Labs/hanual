from __future__ import annotations


from hanual.compile.constants.constant import Constant
from hanual.compile.instruction import *
from hanual.compile.label import Label
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from typing import TYPE_CHECKING
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

    def compile(self, cm):
        instructions = []

        while_start = Label("WHILE", mangle=True)

        instructions.append(while_start)
        instructions.extend(self._while.compile())
        instructions.extend(self.body.compile(cm))
        instructions.append(JIT(while_start))

        return instructions

    def execute(self, scope: Scope) -> Result:
        res = Result()

        while_scope = Scope(parent=scope)

        while True:
            keep_going, err = res.inherit_from(self._while.execute(while_scope))

            if err:
                return res

            if not keep_going:
                return res

            _, err = res.inherit_from(self._body.execute(while_scope))

            if err:
                return res

    def get_constants(self) -> list[Constant]:
        return [*self._while.get_constants(), *self._body.get_constants()]

    def get_names(self) -> list[str]:
        return [*self._while.get_names(), *self._body.get_names()]

    def find_priority(self) -> list[BaseNode]:
        return self._body.find_priority()
