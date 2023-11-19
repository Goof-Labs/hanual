from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack
from hanual.lang.lexer import Token

from .base_node import BaseNode
from .f_call import FunctionCall

if TYPE_CHECKING:
    ...


class ImplicitCondition(BaseNode):
    __slots__ = (
        "_val",
        "_op",
        "_lines",
        "_line_range",
    )

    def __init__(
        self, op: Token, val: Union[Token, FunctionCall], lines: str, line_range: int
    ) -> None:
        self._val: Union[Token, FunctionCall] = val
        self._op: Token = op

        self._line_range = line_range
        self._lines = lines

    @property
    def value(self) -> Union[Token, FunctionCall]:
        return self._val

    @property
    def op(self) -> Token:
        return self._op

    def compile(self, name: str):
        raise NotImplementedError
