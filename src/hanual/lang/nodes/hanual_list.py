from __future__ import annotations

from typing import TYPE_CHECKING, List

from .base_node import BaseNode

if TYPE_CHECKING:
    from .arguments import Arguments

from .arguments import Arguments


class HanualList(BaseNode):
    __slots__ = "_elements", "_lines", "_line_range"

    def __init__(self, args: Arguments, lines: str, line_range: int) -> None:
        self._elements = args

        self._line_range = line_range
        self._lines = lines

    @property
    def elements(self) -> List:
        return self._elements.children

    def compile(self) -> None:
        raise NotImplementedError

    def execute(self, env):
        raise NotImplementedError
