from __future__ import annotations

# from hanual.compile.instruction import (
#    InstructionPK2,
#    InstructionPGA,
#    InstructionCAL,
# )
from typing import Any, TYPE_CHECKING, Dict, Union
from hanual.lang.lexer import Token
from .base_node import BaseNode
from abc import ABC


if TYPE_CHECKING:
    from hanual.compile import Assembler


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

    def compile(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self.get_repr(self._left),
            "right": self.get_repr(self._right),
        }
