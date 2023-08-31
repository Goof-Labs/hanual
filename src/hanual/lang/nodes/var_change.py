from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from hanual.compile.constants.constant import Constant
from hanual.compile.instruction import *
from hanual.compile.registers import Registers
from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    pass

T = TypeVar("T", bound=BaseNode)


class VarChange(BaseNode):
    __slots__ = "_name", "_value",

    def __init__(self: BaseNode, name: Token, value) -> None:
        self._name: Token = name
        self._value: T = value

    @property
    def name(self) -> Token:
        return self._name

    @property
    def value(self) -> T:
        return self._value

    def compile(self):
        instructions = []

        if isinstance(self._value, Token):
            if self._value.type in ("STR", "NUM"):
                instructions.append(
                    MOV_RC[self._name.value, Constant(self._value.value)]
                )

            elif self._value.type == "NME":
                instructions.append(CPY[self._name.value, self._value.value])

            else:
                raise NotImplementedError

        else:
            instructions.extend(self._value.compile())
            instructions.append(MOV_RR[self._name.value, Registers.R])

        return instructions

    def execute(self, env):
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        consts = []

        if isinstance(self._value, Token):
            if self._value.type in ("STR", "NUM"):
                consts.append(Constant(self._value.value))

        else:
            consts.extend(self._value.get_constants())

        return consts

    def get_names(self) -> list[str]:
        return [
            self._name.value,
            *self._value.get_names()
        ]

    def find_priority(self) -> list[BaseNode]:
        # TODO take blocks or lambda functions into account
        return []
