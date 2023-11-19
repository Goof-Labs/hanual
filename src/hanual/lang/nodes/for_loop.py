from __future__ import annotations

from typing import TYPE_CHECKING, Union

from .base_node import BaseNode
from .implicit_binop import ImplicitBinOp
from .implicit_condition import ImplicitCondition

if TYPE_CHECKING:
    from hanual.lang.lexer import Token

    from .assignment import AssignmentNode
    from .block import CodeBlock
    from .conditions import Condition


# for let i=0, < 10, +110
class ForLoop(BaseNode):
    __slots__ = "_while", "_init", "_action", "_body", "_lines", "_line_range"

    def __init__(
        self: BaseNode,
        condition: Union[ImplicitCondition, Condition],
        init: Union[Token, AssignmentNode],
        action: ImplicitBinOp,
        body: CodeBlock,
        lines: str,
        line_range: int,
    ) -> None:
        self._while: Union[ImplicitCondition, Condition] = condition
        self._init: Union[Token, AssignmentNode] = init
        self._action: ImplicitBinOp = action
        self._body: CodeBlock = body

        self._lines = lines
        self._line_range = line_range

    @property
    def condition(self) -> Union[ImplicitCondition, Condition]:
        return self._while

    @property
    def init(self) -> Union[Token, AssignmentNode]:
        return self._init

    @property
    def action(self) -> ImplicitBinOp:
        return self._action

    @property
    def body(self) -> CodeBlock:
        return self._body

    def compile(self):
        raise NotImplementedError

    def get_names(self) -> list[str]:
        names = []

        names.extend(self._action.get_names())
        names.extend(self._while.get_names())
        names.extend(self._init.get_names())
        names.extend(self._body.get_names())

        return names
