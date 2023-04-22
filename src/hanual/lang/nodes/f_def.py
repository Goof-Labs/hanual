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

        entery_point = global_state.labels.new_label(f"FN_{self._name}")
        global_state.add_function(self._name, entery_point)

        if not self._inner:
            return (Instruction(InstructionEnum.RET),)
        return self._inner.compile(global_state), Instruction(InstructionEnum.RET)

    def __str__(self, level=0) -> str:
        return f"{type(self).__name__}(\n{' '.rjust(level)}name = {self._name.__str__(level+1) if issubclass(type(self._name), BaseNode) else str(str(self._name))}\n{' '.rjust(level)} name = {self._name.__str__(level+1) if issubclass(type(self._name), BaseNode) else str(str(self._name))}\n{' '.rjust(level)} inner = {self._inner.__str__(level+1) if issubclass(type(self._inner), BaseNode) else str(str(self._inner))})\n"
