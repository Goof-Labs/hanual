from __future__ import annotations

# from hanual.compile.instruction import Instruction, InstructionPGC
from typing import TypeVar, Generic, Any, Dict
from hanual.lang.lexer import Token
from hanual.compile.ir import IR
from .base_node import BaseNode


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

    def as_dict(self) -> Dict[str, Any]:
        return {
            "type": type(self).__name__,
            "name": self._target,
            "value": self._value.as_dict()
            if hasattr(self._value, "as_dict")
            else self._value,
        }

    def compile(self, ir: IR) -> None:
        var = ir.reg_name(self._target.value)

        if hasattr(self._value, "compile"):
            reg = ir.reserve_reg()

            self._value.compile(to=reg)
            ir.mov(var, reg)

            ir.free_reg(reg)

        else:
            # token or literal
            ir.mov(var, self._value.value)

        # TODO MOVE TO HEAP [var]
