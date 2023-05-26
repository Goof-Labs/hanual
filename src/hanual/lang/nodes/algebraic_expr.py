from __future__ import annotations

from hanual.compile.instruction import (
    InstructionCAL,
    InstructionAFA,
    InstructionFPA,
    InstructionCFA,
)
from typing import Any, Dict, Union, TYPE_CHECKING
from hanual.lang.lexer import Token
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.assembler import Assembler


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
                # get the heap index of the left value
                left_name: int = global_state.heap.index(self._left.value)
                # add it to the function argument register
                global_state.instructions.append(InstructionFPA(left_name))

            elif self._left.type == "NUM":
                global_state.constants.add(self._left.value)
                const_id = list(global_state.constants).index(self._left.value)
                global_state.instructions.append(InstructionFPA(const_id))

            else:
                raise Exception(f"bad token {self._left}")

        elif hasattr(self._left, "compile"):
            self._left.compile(global_state)

        else:
            raise Exception(
                f"{self._left} is not a token and has no attribute 'compile'"
            )

        # RIGHT
        if isinstance(self._rigth, Token):
            if self._rigth.type == "ID":
                # get the heap index of the left value
                left_name: int = global_state.heap.index(self._rigth.value)
                # add it to the function argument register
                global_state.instructions.append(InstructionFPA(left_name))

            elif self._rigth.type == "NUM":
                global_state.constants.add(self._rigth.value)
                const_id = list(global_state.constants).index(self._rigth.value)
                global_state.instructions.append(InstructionFPA(const_id))

            else:
                raise Exception(f"bad token {self._rigth}")

        op_fn = global_state.fn_deps.add(self._op)
        global_state.instructions.append(InstructionFPA(op_fn))
        global_state.add_instructions(InstructionCAL())
