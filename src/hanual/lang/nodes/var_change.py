from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    ...

T = TypeVar("T", bound=BaseNode)


class VarChange(BaseNode):
    __slots__ = (
        "_name",
        "_value",
        "_lines",
        "_line_range",
    )

    def __init__(
        self: BaseNode, name: Token, value, lines: str, line_range: int
    ) -> None:
        self._name: Token = name
        self._value: T = value

        self._line_range = line_range
        self._lines = lines

    @property
    def name(self) -> Token:
        return self._name

    @property
    def value(self) -> T:
        return self._value

    def compile(self):
        raise NotImplementedError
