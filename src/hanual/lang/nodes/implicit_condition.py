from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.lexer import Token

from .base_node import BaseNode
from .f_call import FunctionCall
from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    ...


class ImplicitCondition[O: Token, V: (Token, FunctionCall)](BaseNode):
    __slots__ = (
        "_val",
        "_op",
        "_lines",
        "_line_range",
    )

    def __init__(self, op: O, val: V, lines: str, line_range: int) -> None:
        self._val: V = val
        self._op: O = op

        self._line_range = line_range
        self._lines = lines

    @property
    def value(self) -> V:
        return self._val

    @property
    def op(self) -> O:
        return self._op

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
