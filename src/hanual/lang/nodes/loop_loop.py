from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from hanual.lang.errors import Frame

from .base_node import BaseNode
from .block import CodeBlock

if TYPE_CHECKING:
    ...


class LoopLoop(BaseNode, ABC):
    __slots__ = ("_inner", "_lines", "_line_range")

    def __init__(self, inner: CodeBlock, lines: str, line_range: int) -> None:
        self._inner: CodeBlock = inner

        self._lines = lines
        self._line_range = line_range

    @property
    def inner(self) -> CodeBlock:
        return self._inner

    def compile(self, **kwargs):
        raise NotImplementedError
