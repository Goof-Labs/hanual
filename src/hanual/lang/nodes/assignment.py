from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from hanual.compile.constant import Constant
from hanual.compile.instruction import *
from hanual.compile.registers import Registers
from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    ...

T = TypeVar("T", BaseNode, Token)


class AssignmentNode(BaseNode, Generic[T]):
    __slots__ = ("_target", "_value")

    def __init__(self: BaseNode, target: Token, value: T) -> None:
        self._target: Token = target
        self._value: T = value

    @property
    def target(self) -> Token:
        return self._target

    @property
    def value(self) -> T:
        return self._value

    def compile(self):
        if isinstance(self._value, Token):
            if self._value.type == "ID":
                # if we want to allocate one variable to another we make a coppy, this may change at optim time
                return [CPY[self._target.value, self._value.value]]

            elif self._value.type in ("STR", "NUM"):
                # we move a constant into a register
                return [MOV_RC[self._target.value, self._value.value]]

            else:
                raise NotImplementedError

        else:
            return [*self._value.compile(), CPY[self._target.value, Registers.R]]

    def get_constants(self) -> list[Constant]:
        # if we want to set the value to a literal then we add it as a constant
        if isinstance(self._value, Token):
            if self._value.type in ("STR", "NUM"):
                return [Constant(self._value.value)]

        return []

    def get_names(self) -> list[str]:
        return [self._target.value]

    def execute(self):
        raise NotImplementedError

    def find_priority(self) -> list[BaseNode]:
        return []
