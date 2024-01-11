from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Optional

from .base_node import BaseNode
from hanual.util import Reply, Request, Response, REQUEST_TYPE

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from hanual.lang.lexer import Token


class ReturnStatement[V: (Token, BaseNode)](BaseNode):
    __slots__ = (
        "_value",
        "_lines",
        "_line_range",
    )

    def __init__(self, value: V, lines: str, line_range: LineRange) -> None:
        self._value: V = value

        self._line_range = line_range
        self._lines = lines

    @property
    def value(self) -> V:
        return self._value

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
