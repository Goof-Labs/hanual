from __future__ import annotations

from hanual.lang.builtin import Token
from typing import TypeVar, List, Any
from .base_node import BaseNode

T = TypeVar("T", Token, ...)


class ReturnStatement(BaseNode):
    def __init__(self: BaseNode, value: T) -> None:
        self._value: T = value

    def eval(self: BaseNode, context) -> Any:
        return super().eval(context)

    def compile(self) -> Any:
        return super().compile()

    def __str__(self, level=0) -> str:
        return f"{type(self).__name__}(ret={self._value})"
