from __future__ import annotations

from hanual.compile import GlobalState
from .conditions import Condition
from .base_node import BaseNode
from .block import CodeBlock
from typing import Any


class IfStatement(BaseNode):
    def __init__(self: IfStatement, condition: Condition, if_true: CodeBlock) -> None:
        self._condition = condition
        self._iftrue = if_true

    def compile(self, global_state: GlobalState) -> Any:
        return super().compile(global_state)

    def __str__(self, level=0) -> str:
        return f"{type(self).__name__}(\n{' '.rjust(level)}con = {self._condition.__str__(level+1) if issubclass(type(self._condition), BaseNode) else str(str(self._condition))}\n{' '.rjust(level)} if_true = {self._iftrue.__str__(level+1) if issubclass(type(self._iftrue), BaseNode) else str(str(self._iftrue))}\n"
