from __future__ import annotations

from hanual.lang.builtin_lexer import Token
from typing import TypeVar, List, Any
from .base_node import BaseNode

T = TypeVar("T", Token, ...)


class NamespaceAcessor(BaseNode):
    def __init__(self: BaseNode, first: T) -> None:
        self._path: List[Token] = [first]

    def add_child(self, child: T) -> None:
        self._path.append(child)
        return self

    def eval(self: BaseNode, context) -> Any:
        return super().eval(context)

    def compile(self) -> Any:
        return super().compile()

    def __str__(self, level=0) -> str:
        return f"{type(self).__name__}({' -> '.join(str(i) for i in self._path)})"
