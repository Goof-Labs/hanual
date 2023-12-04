from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from .base_node import BaseNode
from .block import CodeBlock

from hanual.util import Reply, Response, Request


if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class LoopLoop(BaseNode):
    __slots__ = ("_inner", "_lines", "_line_range")

    def __init__(self, inner: CodeBlock, lines: str, line_range: LineRange) -> None:
        self._inner: CodeBlock = inner

        self._lines = lines
        self._line_range = line_range

    @property
    def inner(self) -> CodeBlock:
        return self._inner

    def compile(self) -> Generator[Reply | Request, Response, None]:
        raise NotImplementedError
