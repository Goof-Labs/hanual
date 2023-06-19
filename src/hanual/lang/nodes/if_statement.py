from __future__ import annotations

from typing import Any, TYPE_CHECKING, Dict

from hanual.runtime.runtime import RuntimeEnvironment
from hanual.compile.constant import Constant
from hanual.runtime.status import ExecStatus
from hanual.compile.instruction import *
from hanual.compile.label import Label
from hanual.lang.errors import Error
from .base_node import BaseNode
from .block import CodeBlock
from abc import ABC


if TYPE_CHECKING:
    from hanual.runtime import RuntimeEnvironment, ExecStatus
    from hanual.lang.errors import Error
    from .conditions import Condition
    from .block import CodeBlock


class IfStatement(BaseNode, ABC):
    def __init__(self: IfStatement, condition: Condition, block: CodeBlock) -> None:
        self._condition: Condition = condition
        self._block: CodeBlock = block

    @property
    def condition(self) -> Condition:
        return self._condition

    @property
    def block(self) -> CodeBlock:
        return self._block

    def compile(self) -> None:
        # The asm genorated by this goes
        # CMP [condition]
        # JMP-FALSE IF_lable
        # code
        # code
        # IF_lable
        # This means that we only jump if the condition is false
        instructions = []

        false_lbl = Label("IF", mangle=True)

        instructions.extend(self._condition.compile())  # compare and put into ac

        instructions.append(JIF(false_lbl))

        return instructions

    def get_constants(self) -> list[Constant]:
        consts = []

        consts.extend(self._condition.get_constants())
        consts.extend(self._block.get_constants())

        return consts

    def get_names(self) -> list[Constant]:
        names = []

        names.extend(self._condition.get_names())
        names.extend(self._block.get_names())

        return names

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def find_priority(self) -> list[BaseNode]:
        return self._block.find_priority()

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
