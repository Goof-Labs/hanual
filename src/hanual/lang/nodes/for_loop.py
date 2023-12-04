from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from .base_node import BaseNode
from .implicit_binop import ImplicitBinOp
from .implicit_condition import ImplicitCondition

from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    from hanual.lang.lexer import Token

    from .assignment import AssignmentNode
    from .block import CodeBlock
    from .conditions import Condition


# for let i=0, < 10, +110
class ForLoop[
C: (ImplicitCondition, Condition),
I: (Token, AssignmentNode),
A: ImplicitBinOp,
](BaseNode):
    __slots__ = "_while", "_init", "_action", "_body", "_lines", "_line_range"

    def __init__(
            self,
            condition: C,
            init: I,
            action: A,
            body: CodeBlock,
            lines: str,
            line_range: int,
    ) -> None:
        self._while: C = condition
        self._init: I = init
        self._action: A = action
        self._body: CodeBlock = body

        self._lines = lines
        self._line_range = line_range

    @property
    def condition(self) -> C:
        return self._while

    @property
    def init(self) -> I:
        return self._init

    @property
    def action(self) -> A:
        return self._action

    @property
    def body(self) -> CodeBlock:
        return self._body

    def compile(self) -> Generator[Reply | Request, Response, None]:
        raise NotImplementedError
