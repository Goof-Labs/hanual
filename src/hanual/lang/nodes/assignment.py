from __future__ import annotations

# from hanual.compile.instruction import Instruction, InstructionPGC
from typing import TypeVar, Generic, Any, Dict, TYPE_CHECKING
from hanual.compile.high_level_instructions import MOV
from hanual.lang.lexer import Token
from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.compile.assembler import Assembler


T = TypeVar("T", bound=BaseNode)
A = TypeVar("A")
B = TypeVar("B")


class AssignmentNode(BaseNode, Generic[B]):
    __slots__ = ("_target", "_value")

    def __init__(self: BaseNode, target: Token, value: B) -> None:
        self._target: Token = target
        self._value: B = value

    def compile(self, global_state: Assembler) -> Any:
        if isinstance(self._value, Token):
            if self._value.type == "NUM" or self._value.type == "NUM":
                # MOV [HAP-ADDR], [val]
                global_state.add_name(self._target.value)

                global_state.add_const(self._value.value)

                t_idx = global_state.get_name_idx(self._target.value)

                global_state.add_code(MOV[t_idx, self._value])

            else:
                raise Exception

        else:
            assert hasattr(self._value, "compile")

            self._value.compile(global_state, to="A")

            t_idx = global_state.get_name_idx(self._target.value)

            global_state.add_code(MOV[t_idx, "A"])

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
