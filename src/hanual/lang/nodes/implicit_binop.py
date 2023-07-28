from __future__ import annotations

from hanual.lang.nodes.base_node import BaseNode
from hanual.compile.registers import Registers
from hanual.compile.constant import Constant
from hanual.compile.instruction import *
from typing import Union, TYPE_CHECKING
from hanual.lang.lexer import Token
from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from .f_call import FunctionCall


class ImplicitBinop(BaseNode):
    def __init__(self: BaseNode, op: Token, right: Union[Token, FunctionCall]) -> None:
        # The left side is implied
        self._right = right
        self._op = op

    @property
    def op(self) -> Token:
        return self._op

    @property
    def right(self) -> Union[Token, FunctionCall]:
        return self._right

    def compile(self, name: str):
        instructions = []

        reg_1 = new_reg()
        reg_2 = new_reg()

        # LEFT SIDE
        instructions.append(MOV[reg_2, name])

        # RIGHT SIDE
        if isinstance(self._right, Token):
            if self._right.type in ("STR", "NUM"):
                instructions.append(MOV[reg_2, self._right.value])

            elif self._right.type == "ID":
                instructions.append(MOV[reg_2, self._right.value])

            else:
                raise NotImplementedError

        else:
            instructions.extend(self._right.compile())
            instructions.append(MOV[reg_2, Registers.R])

        instructions.append(EXC[self._op.value, reg_1, reg_2])

        return instructions

    def execute(self):
        raise NotImplementedError

    def get_names(self) -> list[str]:
        if isinstance(self._right, Token):
            if self._right.type == "ID":
                return [self._right.value]

            else:
                return []

        else:
            return self._right.get_names()

    def get_constants(self) -> list[Constant]:
        if isinstance(self._right, Token):
            if self._right.type in ("STR", "NUM"):
                return [Constant(self._right.value)]

        else:
            return self._right.get_constants()

    def find_priority(self):
        return []
