from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
from typing import TypeVar, Generic, Any, Dict
from hanual.compile import Assembler, Stack
from hanual.lang.lexer import Token
from .base_node import BaseNode

T = TypeVar("T", bound=BaseNode)
A = TypeVar("A")
B = TypeVar("B")


class AssignmentNode(BaseNode, Generic[A, B]):
    __slots__ = ("_target", "_value")

    def __init__(self: BaseNode, target: A, value: B) -> None:
        self._target: A = target
        self._value: B = value

    def compile(self, global_state: Assembler) -> Any:
        raise NotImplementedError

        Stack().get_instance().push(self._value)
        res = []

        if isinstance(self._value, Token):  # a literal value
            const_id = global_state.constants.add_const(self._value.value)
            res.append(Instruction(InstructionEnum.PGC, const_id))

        else:  # not a literal
            res.extend(self._value.compile(global_state))

        return res

    @property
    def target(self) -> A:
        return self._target

    @property
    def value(self) -> B:
        return self._value

    def as_dict(self) -> Dict[str, Any]:
        return {
            "type": type(self).__name__,
            "name": self._target,
            "value": self._value.as_dict() if hasattr(self._value, "as_dict") else self._value,
        }
