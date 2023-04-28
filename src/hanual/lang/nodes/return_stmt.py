from __future__ import annotations

from abc import ABC

from hanual.lang.builtin_lexer import Token
from hanual.compile import Assembler
from .base_node import BaseNode
from typing import TypeVar, Any

T = TypeVar("T", Token, ...)


class ReturnStatement(BaseNode, ABC):
    def __init__(self: BaseNode, value: T) -> None:
        self._value: T = value

    def compile(self, global_state: GlobalState) -> Any:
        raise NotImplementedError
        return super().compile(global_state)
