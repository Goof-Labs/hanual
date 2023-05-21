from __future__ import annotations
from hanual.compile import Assembler

from hanual.compile.instruction import (
    InstructionPK2,
    InstructionPGA,
    InstructionCAL,
)
from hanual.lang.lexer import Token
from typing import Any, Dict, Union
from .base_node import BaseNode


class AlgebraicExpression(BaseNode):
    __slots__ = "_op", "_left", "_right"

    def __init__(
        self: BaseNode,
        operator: Token,
        left: Union[AlgebraicExpression, Token],
        right: Union[AlgebraicExpression, Token],
    ) -> None:
        self._op = operator
        self._left = left
        self._right = right

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self.get_repr(self._left),
            "right": self.get_repr(self._right),
        }

    def compile(self, global_state: Assembler) -> Any:
        # LEFT
        if isinstance(self._left, Token):
            if self._left.type == "ID":
                global_state.pull_value(self._left.value)

            elif self._left.type == "NUM":
                num_id = global_state.add_constant(self._left.value)
                global_state.push_value(num_id)

            else:
                raise Exception(f"bad token {self._left}")

        elif hasattr(self._left, "compile"):
            self._left.compile(global_state)

        else:
            raise Exception(
                f"{self._left} is not a token and has no attribute 'compile'"
            )

        # RIGHT
        if isinstance(self._right, Token):
            if self._right.type == "ID":
                global_state.pull_value(self._right)

            elif self._right.type == "NUM":
                num_id = global_state.add_constant(self._right.value)
                global_state.push_value(num_id)

            else:
                raise Exception(f"bad token {self._right}")

        elif hasattr(self._right, "compile"):
            self._right.compile(global_state)

        else:
            raise Exception(
                f"{self._left} is not a token and has no attribute 'compile'"
            )

        # assuming that the value of both the left and right have been pushed onto the stack we will
        # call the operator as a function

        global_state.add_instructions(InstructionPK2())

        op_fn = global_state.add_function(self._op)
        global_state.add_instructions(InstructionPGA(op_fn))
        global_state.add_instructions(InstructionCAL())
