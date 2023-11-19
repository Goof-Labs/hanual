from __future__ import annotations

from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.nodes.block import CodeBlock
    from hanual.lang.nodes.conditions import Condition


class WhileStatement(BaseNode):
    __slots__ = (
        "_while",
        "_body",
        "_lines",
        "_line_no",
    )

    def __init__(
        self: BaseNode, condition: Condition, body: CodeBlock, lines: str, line_no: int
    ) -> None:
        self._while: Condition = condition
        self._body: CodeBlock = body

        self._line_no = line_no
        self._lines = lines

    @property
    def condition(self) -> Condition:
        return self._while

    @property
    def body(self) -> CodeBlock:
        return self._body

    def compile(self):
        raise NotImplementedError
