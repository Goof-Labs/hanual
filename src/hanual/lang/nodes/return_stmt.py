from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
from hanual.lang.builtin_lexer import Token
from typing import Dict, Any, TYPE_CHECKING
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from hanual.compile import Assembler


class ReturnStatement(BaseNode, ABC):
    def __init__(self: BaseNode, value) -> None:
        self._value = value

    def compile(self, global_state: Assembler) -> Any:
        if isinstance(self._value, Token):
            if self._value.type == "ID":
                global_state.pull_value(self._value.value)

            elif self._value.type in ("STR", "NUM"):
                # get the
                ident = global_state.add_constant(self._value.value)
                global_state.add_instructions(Instruction(InstructionEnum.PGC, ident))

        else:
            self._value.compile(global_state)

    def as_dict(self) -> Dict[str, Any]:
        return {"value": self._value}
