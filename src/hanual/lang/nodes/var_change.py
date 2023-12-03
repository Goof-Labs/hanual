from __future__ import annotations

from typing import TYPE_CHECKING
from hanual.lang.lexer import Token
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class VarChange[V: (BaseNode, Token)](BaseNode):
    __slots__ = (
        "_name",
        "_value",
        "_lines",
        "_line_range",
    )

    def __init__(self, name: Token, value: V, lines: str, line_range: LineRange) -> None:
        self._name: Token = name
        self._value: V = value

        self._line_range = line_range
        self._lines = lines

    @property
    def name(self) -> Token:
        return self._name

    @property
    def value(self) -> V:
        return self._value

    def compile(self):
        raise NotImplementedError
