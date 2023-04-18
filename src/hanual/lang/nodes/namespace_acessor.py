from __future__ import annotations

from hanual.lang.builtin_lexer import Token
from typing import TypeVar, List, Any, Self
from .base_node import BaseNode

T = TypeVar("T", Token, ...)


class NamespaceAcessor(BaseNode):
    def __init__(self: BaseNode, first: T) -> None:
        self._path: List[Token] = [first]

    def add_child(self, child: T) -> Self:
        self._path.append(child)
        return self

    def compile(self, global_state) -> Any:
        return super().compile(global_state)

    def __str__(self, level=0) -> str:
        return f"{type(self).__name__}({' -> '.join(str(i) for i in self._path)})"
