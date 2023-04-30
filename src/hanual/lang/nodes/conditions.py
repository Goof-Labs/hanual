from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
from typing import Any, Dict, TYPE_CHECKING
from hanual.lang.lexer import Token
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from hanual.compile import Assembler


class Condition(BaseNode, ABC):
    __slots__ = "_op", "_left", "_right"

    def __init__(self: BaseNode, op: Token, left, right) -> None:
        self._right = right
        self._left = left
        self._op = op

    @property
    def op(self):
        return self._op

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def compile(self, global_state: Assembler) -> Any:
        if isinstance(self._left, Token):
            cid = global_state.add_constant(self._left)
            global_state.add_instructions(Instruction(InstructionEnum.PGC, cid))

        else:
            assert hasattr(self._left, "compile")
            self._left.compile(global_state)

        if isinstance(self._right, Token):
            cid = global_state.add_constant(self._right)
            global_state.add_instructions(Instruction(InstructionEnum.PGC, cid))

        else:
            assert hasattr(self._right, "compile")
            self._right.compile(global_state)

        op_id = global_state.add_function(self._op.value)  # one of +-/*% and yes these are functions now

        global_state.add_instructions(Instruction(InstructionEnum.PK2))
        global_state.add_instructions(Instruction(InstructionEnum.PGA, op_id))
        global_state.add_instructions(Instruction(InstructionEnum.CAL))

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self._left,
            "right": self._right,
        }
