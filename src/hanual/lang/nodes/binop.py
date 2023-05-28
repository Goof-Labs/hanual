from __future__ import annotations

from typing import Any, TYPE_CHECKING, Dict, Union
from hanual.lang.lexer import Token
from .base_node import BaseNode
from abc import ABC


if TYPE_CHECKING:
    from hanual.compile.ir import IR


class BinOpNode(BaseNode, ABC):
    __slots__ = "_right", "_left", "_op"

    def __init__(self, op: Token, left, right) -> None:
        self._right: Union[Token, BinOpNode] = right
        self._left: Union[Token, BinOpNode] = left

        self._op: Token = op

    @property
    def left(self):
        """The left property."""
        return self._left

    @property
    def right(self):
        """The right property."""
        return self._right

    @property
    def op(self):
        """The op property."""
        return self._op

    def compile(self, ir: IR, to: str = None) -> None:
        if hasattr(self._left, "compile"):
            self._left.compile(ir, to="FA")

        else:
            if self._left.type == "NUM":
                ir.mov("FA", ir.int_con(self._left.value))

            else:
                ir.mov("FA", ir.find_name(self._left.value))

        if hasattr(self._right, "compile"):
            self._right.compile(ir, to="FA")

        else:
            if self._right.type == "NUM":
                ir.mov("FA", ir.int_con(self._right.value))

            else:
                ir.mov("FA", ir.find_name(self._right.value))

        ir.mov("FP", self._op.value)
        ir.call()

        if not to is None:
            ir.mov(to, "AC")

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self.get_repr(self._left),
            "right": self.get_repr(self._right),
        }
