from __future__ import annotations

from hanual.compile import GlobalState
from typing import TypeVar, Any, Dict
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
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return {
            "args": self._arguments.as_dict(),
            "name": self._name,
            "inner": self._inner.as_dict()
            if hasattr(self._inner, "as_dict")
            else self._inner,
        }
