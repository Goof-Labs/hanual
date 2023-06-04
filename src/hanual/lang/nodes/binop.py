from __future__ import annotations

from typing import Any, TYPE_CHECKING, Dict, Union
from hanual.lang.errors import Error
from hanual.lang.lexer import Token
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
from .base_node import BaseNode
from abc import ABC


if TYPE_CHECKING:
    from hanual.compile.state_fragment import Fragment


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
        frag = Fragment()

        if isinstance(self._left, Token):
            ...

        else:
            assert hasattr(
                self._left, "compile"
            ), f"{self._left} needs a compile method or be a token"
            self._left.compile()

        return frag

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "op": self._op,
            "left": self.get_repr(self._left),
            "right": self.get_repr(self._right),
        }
