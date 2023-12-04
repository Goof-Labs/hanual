from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from .base_node import BaseNode
from hanual.util import Reply, Response, Request

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

    def compile(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
