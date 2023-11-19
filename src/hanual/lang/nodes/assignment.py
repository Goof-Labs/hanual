from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator, Generic, TypeVar

from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack
from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    ...

T = TypeVar("T", BaseNode, Token)


class AssignmentNode(BaseNode, Generic[T]):
    __slots__ = ("_target", "_value", "_lines", "_line_range")

    def __init__(
        self: BaseNode, target: Token, value: T, lines: str, line_range: int
    ) -> None:
        self._target: Token = target
        self._value: T = value

        self._line_range = line_range
        self._lines = lines

    @property
    def target(self) -> Token:
        return self._target

    @property
    def value(self) -> T:
        return self._value

    def compile(self):
        raise NotImplementedError
