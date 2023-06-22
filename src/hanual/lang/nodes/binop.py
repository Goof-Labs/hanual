from __future__ import annotations

from typing import Any, TYPE_CHECKING, Dict, Union
from hanual.compile.constant import Constant
from hanual.lang.errors import Error
from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
from .base_node import BaseNode
from hanual.compile.instruction import *
from abc import ABC


if TYPE_CHECKING:
    ...


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

    def compile(self) -> None:
        instructions = []

        reg_1 = new_reg()
        reg_2 = new_reg()

        # LEFT SIDE
        if isinstance(self._left, Token):
            if self._left.type in ("STR", "NUM"):
                instructions.append(MOV[reg_1, self._left.value])

            elif self._left.type == "ID":
                instructions.append(MOV[reg_2, self._left.value])

            else:
                raise NotImplementedError

        else:
            instructions.extend(self._left.compile())
            instructions.append(MOV[reg_1, "AC"])

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
            instructions.append(MOV[reg_2, "AC"])

        instructions.append(EXC[self._op.value, reg_1, reg_2])
        return instructions

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def get_constants(self) -> list[Constant]:
        consts = []

        if isinstance(self._left, Token):
            if self._left.type in ("STR", "NUM"):
                consts.append(self._left.value)

        else:
            consts.extend(self._left.get_constants())

        if isinstance(self._right, Token):
            if self._right.type in ("STR", "NUM"):
                consts.append(self._right.value)

        else:
            consts.extend(self._right.get_constants())

        return consts

    def get_names(self) -> list[str]:
        names = []

        if isinstance(self._left, Token):
            if self._left.type == "ID":
                names.append(self._left.value)

        if isinstance(self._right, Token):
            if self._right == "ID":
                names.append(self._right.value)

        return names

    def find_priority(self) -> list[BaseNode]:
        return []

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self.get_repr(self._left),
            "right": self.get_repr(self._right),
        }
