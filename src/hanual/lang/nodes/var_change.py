from __future__ import annotations


from typing import Any, Dict, TypeVar, TYPE_CHECKING
from hanual.lang.lexer import Token
from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.compile.ir import IR

T = TypeVar("T", bound=BaseNode)


class VarChange(BaseNode):
    def __init__(self: BaseNode, name: Token, value) -> None:
        self._name: Token = name
        self._value: T = value

    @property
    def name(self) -> Token:
        return self._name

    @property
    def value(self) -> T:
        return self._value

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()

    def compile(self, ir: IR) -> None:
        reg = ir.reserve_reg()

        if isinstance(self._value, Token):
            ir.mov(reg, self._value.value)

        else:
            self._value.compile(ir, to=reg)

        name = ir.find_name(self._name.value)

        ir.mov(name, reg)

        ir.free_reg(reg)
