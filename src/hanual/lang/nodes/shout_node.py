from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Optional

from .base_node import BaseNode
from hanual.util import Reply, Request, Response, REQUEST_TYPE

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from hanual.lang.lexer import Token


class ShoutNode(BaseNode):
    __slots__ = (
        "_st",
        "_lines",
        "_line_range",
    )

    def __init__(self, shout_token: Token, lines: str, line_range: LineRange) -> None:
        self._st = shout_token

        self._line_range = line_range
        self._lines = lines

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
