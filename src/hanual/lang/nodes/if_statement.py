from __future__ import annotations

from abc import ABC

from hanual.compile import Assembler
from .conditions import Condition
from .base_node import BaseNode
from .block import CodeBlock
from typing import Any


class IfStatement(BaseNode, ABC):
    def __init__(self: IfStatement, condition: Condition, if_true: CodeBlock) -> None:
        self._condition = condition
        self._iftrue = if_true

    def compile(self, global_state: Assembler) -> Any:
        raise NotImplementedError
        return super().compile(global_state)
