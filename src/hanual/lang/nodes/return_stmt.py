from __future__ import annotations

from hanual.compile.compile import GlobalState
from hanual.lang.builtin_lexer import Token
from .base_node import BaseNode
from typing import TypeVar, Any

T = TypeVar("T", Token, ...)


class ReturnStatement(BaseNode):
    def __init__(self: BaseNode, value: T) -> None:
        self._value: T = value

    def compile(self, global_state: GlobalState) -> Any:
        return super().compile(global_state)
