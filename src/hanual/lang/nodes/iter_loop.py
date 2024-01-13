from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from hanual.lang.util.line_range import LineRange

    from .f_call import FunctionCall


class IterLoop[I: (Token, FunctionCall)](BaseNode):
    def __init__(
        self, name: Token, iterator: I, lines: str, line_range: LineRange
    ) -> None:
        self._iterator: I = iterator
        self._name: Token = name

        self._lines = lines
        self._line_range = line_range

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
