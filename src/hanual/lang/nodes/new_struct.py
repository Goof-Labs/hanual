from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from hanual.lang.util.line_range import LineRange

    from .arguments import Arguments
    from .f_call import FunctionCall


class NewStruct(BaseNode):
    __slots__ = "_args", "_name", "_line_range", "_lines"

    def __init__(self, call: FunctionCall, lines: str, line_range: LineRange) -> None:
        self._args: Arguments = call.args
        self._name: Token = call.name

        self._line_range = line_range
        self._lines = lines

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
