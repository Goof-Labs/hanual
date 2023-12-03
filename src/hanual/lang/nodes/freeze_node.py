from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    ...


class FreezeNode[T: Token](BaseNode, ABC):
    __slots__ = "_var", "_lines", "_line_no"

    def __init__(self, var: T, lines: str, line_no: int) -> None:
        self._var: T = var

        self._line_no = line_no
        self._lines = lines

    def compile(self) -> None:
        raise NotImplementedError

    @property
    def target(self):
        return self._var
