from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
from hanual.compile import GlobalState, Stack
from typing import TypeVar, Generic, Any
from hanual.lang.lexer import Token
from .base_node import BaseNode

T = TypeVar("T", bound=BaseNode)
A = TypeVar("A")
B = TypeVar("B")


class AssighnmentNode(BaseNode, Generic[A, B]):
    __slots__ = ("_target", "_value")

    def __init__(self: BaseNode, target: A, value: B) -> None:
        self._target: A = target
        self._value: B = value

    def compile(self, global_state: GlobalState) -> Any:
        Stack().get_instance().push(self._target.value)  # push name record to stack

        if isinstance(self._value, Token):
            id = global_state.constants.add_const(self._value.value)
            return (Instruction(InstructionEnum.PGC, id),)

        return (Instruction(InstructionEnum.PGC, self._value.compile(global_state)),)

    @property
    def target(self) -> A:
        return self._target

    @property
    def value(self) -> B:
        return self._value

    def __str__(self, level=0) -> str:
        return f"{type(self).__name__.rjust(level+1)}(\n{' '.rjust(level)}target = {self.target.__str__(level+1) if issubclass(type(self.target), BaseNode) else str(str(self.target))}\n{' '.rjust(level)}value = {self.value.__str__(level+1) if issubclass(type(self.value), BaseNode) else str(str(self.value))}\n{' '.rjust(level)})\n"
