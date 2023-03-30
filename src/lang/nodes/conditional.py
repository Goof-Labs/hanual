from __future__ import annotations

from .conditions import condition
from .base_node import BaseNode


class Conditional(BaseNode):
    def __init__(self: Conditional, condition: Condition, if_true: Block) -> None:
        self._condition = condition
        self._iftrue = if_true

