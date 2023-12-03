from __future__ import annotations

from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token


class StrongField[T](BaseNode):
    __slots__ = (
        "_name",
        "_type",
        "_lines",
        "_line_range",
    )

    def __init__(
            self: BaseNode, name: Token, type_: T, lines: str, line_range: int
    ) -> None:
        self._name: Token = name
        self._type: T = type_

        self._line_range = line_range
        self._lines = lines

    @property
    def name(self) -> Token:
        return self._name

    @property
    def type(self) -> T:
        return self._type

    def compile(self) -> None:
        return super().compile()
