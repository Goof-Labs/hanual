from __future__ import annotations

# from hanual.compile.instruction import InstructionPGC, InstructionPGA
from hanual.lang.builtin_lexer import Token
from typing import Dict, Any, TYPE_CHECKING
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from hanual.compile import Assembler


class ReturnStatement(BaseNode, ABC):
    def __init__(self: BaseNode, value) -> None:
        self._value = value

    def compile(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return {"value": self._value}
