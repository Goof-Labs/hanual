from __future__ import annotations

from hanual.compile.instruction import (
    InstructionPK2,
    InstructionPGA,
    InstructionCAL,
)
from typing import Any, TYPE_CHECKING, Dict, Union
from hanual.lang.lexer import Token
from .base_node import BaseNode
from abc import ABC


if TYPE_CHECKING:
    from hanual.compile import Assembler


class BinOpNode(BaseNode, ABC):
    __slots__ = "_right", "_left", "_op"

    def __init__(self, op: Token, left, right) -> None:
        self._right: Union[Token, BinOpNode] = right
        self._left: Union[Token, BinOpNode] = left

        self._op: Token = op

    @property
    def left(self):
        """The left property."""
        return self._left

    @property
    def right(self):
        """The right property."""
        return self._right

    @property
    def op(self):
        """The op property."""
        return self._op

    def compile(self, global_state: Assembler) -> Any:
        # LEFT
        if isinstance(self._left, Token):
            if self._left.type == "ID":  # It it is an ID then we hoist
                global_state.pull_value(self._left.value)

            elif self._left.type == "NUM":
                id_ = global_state.add_constant(self._left.value)
                global_state.push_value(id_)

            else:
                raise Exception

        elif hasattr(self._left, "compile"):
            self._left.compile(global_state)

        else:
            raise Exception

        # RIGHT
        if isinstance(self._right, Token):
            if self._right.type == "ID":  # It it is an ID then we hoist
                global_state.pull_value(self._right.value)

            elif self._right.type == "NUM":
                id_ = global_state.add_constant(self._right.value)
                global_state.push_value(id_)

            else:
                raise NotImplementedError

        elif hasattr(self._right, "compile"):
            self._right.compile(global_state)

        else:
            raise Exception

        global_state.add_instructions(InstructionPK2())

        fn_id = global_state.add_reference(self._op.value)
        global_state.add_instructions(InstructionPGA(fn_id))
        global_state.add_instructions(InstructionCAL())

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self.get_repr(self._left),
            "right": self.get_repr(self._right),
        }
