from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from hanual.lang.errors.trace_back import Frame

from .base_node import BaseNode

if TYPE_CHECKING:
    from .block import CodeBlock
    from .conditions import Condition


class ElifStatement(BaseNode, ABC):
    __slots__ = (
        "_condition",
        "_block",
        "_lines",
        "_line_no",
    )

    def __init__(
        self, condition: Condition, block: CodeBlock, lines: str, line_no: int
    ) -> None:
        self._condition = condition
        self._block = block

        self._line_no = line_no
        self._lines = lines

    @property
    def condition(self) -> Condition:
        return self._condition

    @property
    def block(self) -> CodeBlock:
        return self._block

    def compile(self) -> None:
        raise NotImplementedError
