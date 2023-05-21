from __future__ import annotations

from hanual.compile.instruction import (
    InstructionPGC,
    InstructionPK2,
    InstructionPGA,
    InstructionCAL,
)
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
        # LEFT
        if isinstance(self._left, Token):
            if self._left.type == "NUM":
                cid = global_state.add_constant(self._left.value)
                global_state.add_instructions(InstructionPGC(cid))

            elif self._left.type == "ID":
                global_state.pull_value(self._left.value)

            else:
                raise NotImplementedError

        else:
            self._left.compile(global_state)

        # RIGHT
        if isinstance(self._right, Token):
            if self._right.type == "NUM":
                cid = global_state.add_constant(self._right.value)
                global_state.add_instructions(InstructionPGC(cid))

            elif self._right.type == "ID":
                global_state.pull_value(self._right.value)

        else:
            self._right.compile(global_state)

        # pack left and right into tuple
        global_state.add_instructions(InstructionPK2())

        # one of +-/*% and yes these are functions now
        op_id = global_state.add_reference(self._op.value)
        global_state.add_instructions(InstructionPGA(op_id))
        global_state.add_instructions(InstructionCAL())

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self._left,
            "right": self._right,
        }
