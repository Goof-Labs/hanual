from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.nodes.base_node import BaseNode

from hanual.util import Reply, Request


if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from hanual.lang.lexer import Token

    from .f_call import FunctionCall


class IterLoop[I: (Token, FunctionCall)](BaseNode):
    def __init__(
        self, name: Token, iterator: I, lines: str, line_range: LineRange
    ) -> None:
        self._iterator: I = iterator
        self._name: Token = name

        self._lines = lines
        self._line_range = line_range

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Request, Reply, None]:
        raise NotImplementedError
