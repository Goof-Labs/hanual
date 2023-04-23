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
        Stack().get_instance().push(self._value)
        res = []

        if isinstance(self._value, Token):  # a literal value
            id = global_state.constants.add_const(self._value.value)
            res.append(Instruction(InstructionEnum.PGC, id))

        else:  # not a literal
            res.extend(self._value.compile(global_state))

        return res

    @property
    def target(self) -> A:
        return self._target

    @property
    def value(self) -> B:
        return self._value

    def as_dict(self) -> None:
        return {
            "type": type(self).__name__,
            "name": self._target,
            "value": self._value.as_dict(),
        }
