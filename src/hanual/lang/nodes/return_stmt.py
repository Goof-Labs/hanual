from __future__ import annotations

from abc import ABC

from hanual.lang.builtin_lexer import Token
from hanual.compile import Assembler
from .base_node import BaseNode
from typing import Dict, TypeVar, Any

T = TypeVar("T", Token, ...)


class ReturnStatement(BaseNode, ABC):
    def __init__(self: BaseNode, value: T) -> None:
        self._value: T = value

    def compile(self, global_state: Assembler) -> Any:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return {"value": self._value}
