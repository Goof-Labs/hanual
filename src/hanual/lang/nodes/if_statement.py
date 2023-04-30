from __future__ import annotations

from abc import ABC

from typing import Any, TYPE_CHECKING
from .base_node import BaseNode
from .block import CodeBlock


if TYPE_CHECKING:
    from .conditions import Condition
    from hanual.compile import Assembler


class IfStatement(BaseNode, ABC):
    def __init__(self: IfStatement, condition: Condition, if_true: CodeBlock) -> None:
        self._condition = condition
        self._iftrue = if_true

    def compile(self, global_state: Assembler) -> Any:
        raise NotImplementedError
