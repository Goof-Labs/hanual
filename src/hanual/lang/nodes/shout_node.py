from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from .base_node import BaseNode
from hanual.util import Reply, Response, Request

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

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
