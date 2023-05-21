from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionPGC
from typing import TypeVar, Generic, Any, Dict, TYPE_CHECKING
from hanual.lang.lexer import Token
from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.compile import Assembler


T = TypeVar("T", bound=BaseNode)
A = TypeVar("A")
B = TypeVar("B")


class AssignmentNode(BaseNode, Generic[B]):
    __slots__ = ("_target", "_value")

    def __init__(self: BaseNode, target: Token, value: B) -> None:
        self._target: Token = target
        self._value: B = value

    def compile(self, global_state: Assembler) -> Any:
        global_state.push_value(self._target.value)

        if isinstance(self._target, Token):
            ident = global_state.add_constant(self._value.value)
            global_state.add_instructions(InstructionPGC(ident))

        else:
            self._value.compile(global_state)

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
            "value": self._value.as_dict()
            if hasattr(self._value, "as_dict")
            else self._value,
        }
