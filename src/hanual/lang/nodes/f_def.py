from __future__ import annotations

from hanual.compile import GlobalState
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

    def compile(self, global_state: GlobalState) -> Any:
        return super().compile(global_state)

    def __str__(self, level=0) -> str:
        return f"{type(self).__name__}(\n{' '.rjust(level)}name = {self._name.__str__(level+1) if issubclass(type(self._name), BaseNode) else str(str(self._name))}\n{' '.rjust(level)} name = {self._name.__str__(level+1) if issubclass(type(self._name), BaseNode) else str(str(self._name))}\n{' '.rjust(level)} inner = {self._inner.__str__(level+1) if issubclass(type(self._inner), BaseNode) else str(str(self._inner))})\n"
