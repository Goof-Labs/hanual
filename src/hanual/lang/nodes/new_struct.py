from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Optional

from .base_node import BaseNode
from hanual.util import Reply, Request, Response, REQUEST_TYPE

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange

    from hanual.lang.lexer import Token
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

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
