from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from hanual.lang.lexer import Token


class ReturnStatement[V: (Token, BaseNode)](BaseNode, ABC):
    __slots__ = (
        "_value",
        "_lines",
        "_line_range",
    )

    def __init__(self, value: V, lines: str, line_range: LineRange) -> None:
        self._value: V = value

        self._line_range = line_range
        self._lines = lines

    @property
    def value(self) -> V:
        return self._value

    def compile(self) -> None:
        raise NotImplementedError
