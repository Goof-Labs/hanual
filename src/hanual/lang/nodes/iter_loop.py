from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from hanual.lang.lexer import Token

    from .f_call import FunctionCall


class IterLoop[I: (Token, FunctionCall)](BaseNode, ABC):
    def __init__(
            self, name: Token, iterator: I, lines: str, line_range: LineRange
    ) -> None:
        self._iterator: I = iterator
        self._name: Token = name

        self._lines = lines
        self._line_range = line_range

    def compile(self):
        raise NotImplementedError
