from __future__ import annotations

from typing import TYPE_CHECKING, Union

from hanual.lang.lexer import Token

from .base_node import BaseNode
from .dot_chain import DotChain

if TYPE_CHECKING:
    from .arguments import Arguments


class FunctionCall(BaseNode):
    __slots__ = (
        "_name",
        "_args",
        "_lines",
        "_line_range",
    )

    def __init__(
        self, name: Token, arguments: Arguments, lines: str, line_range: int
    ) -> None:
        self._name: Union[Token, DotChain] = name
        self._args: Arguments = arguments

        self._line_range = line_range
        self._lines = lines

    @property
    def name(self) -> Union[Token, DotChain]:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def compile(self):
        raise NotImplementedError
