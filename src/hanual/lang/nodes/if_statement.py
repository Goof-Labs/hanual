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
