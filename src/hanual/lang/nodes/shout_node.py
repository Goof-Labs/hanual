from __future__ import annotations

from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token


class ShoutNode(BaseNode):
    __slots__ = (
        "_st",
        "_lines",
        "_line_range",
    )

    def __init__(
        self: BaseNode, shout_token: Token, lines: str, line_range: int
    ) -> None:
        self._st = shout_token

        self._line_range = line_range
        self._lines = lines

    def compile(self):
        raise NotImplementedError
