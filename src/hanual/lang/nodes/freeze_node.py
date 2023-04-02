from __future__ import annotations


from hanual.lang.lexer import Token
from .base_node import BaseNode
from typing import TypeVar, Any


T = TypeVar("T", bound=Token)


class FreezeNode(BaseNode):
    __slots__ = "_var"

    def __init__(self: BaseNode, var: T) -> None:
        self._var: T = var

    def eval(self: BaseNode, context) -> Any:
        return super().eval(context)

    def compile(self) -> Any:
        return super().compile()

    @property
    def target(self):
        return self._var

    def __str__(self, level=0) -> str:
        return f"\n{type(self).__name__}(\n{' '.rjust(level+1)}freeze = {self.target})"
