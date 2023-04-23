from __future__ import annotations

from hanual.compile import GlobalState
from .base_node import BaseNode
from typing import Any, TypeVar

O = TypeVar("O")
L = TypeVar("L")
R = TypeVar("R")


class Condition(BaseNode):
    __slots__ = "_op", "_left", "_right"

    def __init__(self: BaseNode, op: O, left: L, right: R) -> None:
        self._right = right
        self._left = left
        self._op = op

    @property
    def op(self) -> O:
        return self._op

    @property
    def left(self) -> L:
        return self._left

    @property
    def right(self) -> R:
        return self._right

    def compile(self, global_state: GlobalState) -> Any:
        return super().compile(global_state)
