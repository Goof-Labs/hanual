from __future__ import annotations

from abc import ABC

from typing import Any, Dict, TYPE_CHECKING
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile import Assembler
    from hanual.lang.lexer import Token


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

    def compile(self, global_state: Assembler) -> Any:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self._left,
            "right": self._right,
        }
