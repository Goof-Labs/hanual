from __future__ import annotations
from hanual.lang.nodes.base_node import BaseNode

from hanual.runtime.runtime import RuntimeEnvironment
from typing import Any, Dict, TYPE_CHECKING, Union
from hanual.compile.constant import Constant
from hanual.runtime.status import ExecStatus
from hanual.compile.instruction import *
from hanual.lang.lexer import Token
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from hanual.runtime import RuntimeEnvironment, ExecStatus
    from hanual.lang.errors import Error


class Condition(BaseNode, ABC):
    __slots__ = "_op", "_left", "_right"

    def __init__(self: BaseNode, op: Token, left, right) -> None:
        self._right: Union[Token, BaseNode] = right
        self._left: Union[Token, BaseNode] = left
        self._op: Token = op

    @property
    def op(self):
        return self._op

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def compile(self) -> None:
        instructions = []
        # LEFT SIDE

        reg_l = new_reg()
        reg_r = new_reg()

        if isinstance(self._left, Token):
            if self._left.type in ("STR", "INT"):
                instructions.append(MOV[reg_l, self._left.value])

            elif self._left.type == "ID":
                instructions.append(CPY[reg_l, self._left.value])

        else:
            instructions.extend(self._left.compile())
            instructions.append(MOV[reg_l, "AC"])

        # RIGHT SIDE
        if isinstance(self._right, Token):
            if self._right.type in ("STR", "INT"):
                instructions.append(MOV[reg_r, self._right.value])

            elif self._right.type == "ID":
                instructions.append(CPY[reg_r, self._right.value])

        else:
            instructions.extend(self._right.compile())
            instructions.append(MOV[reg_r, "AC"])

        instructions.append(EXC[self._op.value, reg_l, reg_r])
        instructions.append(CMP[None])

        return instructions

    def get_constants(self) -> list[Constant]:
        consts = []

        if isinstance(self._left, Token):
            if self._left.type in ("STR", "NUM"):
                consts.append(Constant(self._left.value))

        else:
            consts.extend(self._left.get_constants())

        if isinstance(self._right, Token):
            if self._right.type in ("STR", "NUM"):
                consts.append(Constant(self._right.value))

        else:
            consts.extend(self._left.get_constants())

        return consts

    def get_names(self) -> list[str]:
        names = []

        if isinstance(self._left, Token):
            if self._left.type == "ID":
                names.append(self._left.value)

        else:
            names.extend(self._left.get_names())

        if isinstance(self._right, Token):
            if self._right.type == "ID":
                names.append(self._right.value)

        else:
            names.extend(self._right.get_names())

        return names

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def find_priority(self) -> list[BaseNode]:
        return []

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self._left,
            "right": self._right,
        }
