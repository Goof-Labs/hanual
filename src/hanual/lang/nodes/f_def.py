from __future__ import annotations

from hanual.compile.instruction import Instruction, InstructionEnum
from hanual.compile import GlobalState
from .arguments import Arguments
from .base_node import BaseNode
from typing import TypeVar, Any
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
