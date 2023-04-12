from __future__ import annotations

from typing import TypeVar, Any
from .arguments import Arguments
from .base_node import BaseNode
from .block import CodeBlock

T = TypeVar("T")


class FunctionDefinition(BaseNode):
    __slots__ = "_name", "_arguments", "_inner"

    def __init__(
        self: FunctionDefinition, name: T, args: Arguments, inner: CodeBlock
    ) -> None:
        self._arguments = args
        self._inner = inner
        self._name = name  # Token

    def eval(self: BaseNode, context) -> Any:
        return super().eval(context)

    def compile(self) -> Any:
        return super().compile()

    def __str__(self, level=0) -> str:
        return f"{type(self).__name__}(\n{' '.rjust(level)}name = {self.name.__str__(level+1) if issubclass(type(self.name), BaseNode) else str(str(self.name))}\n{' '.rjust(level)} name = {self.name.__str__(level+1) if issubclass(type(self.name), BaseNode) else str(str(self.name))}\n{' '.rjust(level)} inner = {self.inner.__str__(level+1) if issubclass(type(self.inner), BaseNode) else str(str(self.inner))})\n"
