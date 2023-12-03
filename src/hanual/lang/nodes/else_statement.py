from __future__ import annotations

from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from .block import CodeBlock


class ElseStatement(BaseNode):
    __slots__ = (
        "_body",
        "_lines",
        "_line_range",
    )

    def __init__(self, body: CodeBlock, lines: str, line_range: LineRange) -> None:
        self._body = body

        self._line_range = line_range
        self._lines = lines

    @property
    def body(self) -> CodeBlock:
        return self._body

    def compile(self, cm):
        raise NotImplementedError
