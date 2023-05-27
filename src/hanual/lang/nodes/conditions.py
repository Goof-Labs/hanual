from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING
from hanual.lang.lexer import Token
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from hanual.compile.ir import IR


class Condition(BaseNode, ABC):
    __slots__ = "_op", "_left", "_right"

    def __init__(self: BaseNode, op: Token, left, right) -> None:
        self._right = right
        self._left = left
        self._op = op

    @property
    def op(self):
        return self._op

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def compile(self, ir: IR) -> None:
        if hasattr(self._left, "compile"):
            self._left.compile(ir, to="FA")

        else:
            ir.mov("FA", self._left.value)

        if hasattr(self._left, "compile"):
            self._left.compile(ir, to="FA")

        else:
            ir.mov("FA", self._right.value)

        ir.mov("FP", self._op.value)
        ir.call()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self._left,
            "right": self._right,
        }
