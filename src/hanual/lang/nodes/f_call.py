from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.lexer import Token

from .base_node import BaseNode
from .dot_chain import DotChain

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from .arguments import Arguments


class FunctionCall[N: (Token, DotChain)](BaseNode):
    __slots__ = (
        "_name",
        "_args",
        "_lines",
        "_line_range",
    )

    def __init__(
            self,
            name: N,
            arguments: Arguments,
            lines: str,
            line_range: LineRange,
    ) -> None:
        self._name: N = name
        self._args: Arguments = arguments

        self._line_range = line_range
        self._lines = lines

    @property
    def name(self) -> N:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def compile(self):
        raise NotImplementedError
