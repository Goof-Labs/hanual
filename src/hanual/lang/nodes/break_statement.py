from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Self, Generator

from hanual.util import Request, Response, Reply

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode


if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class BreakStatement(BaseNode):
    __slots__ = (
        "_lines",
        "_line_range",
    )

    def __init__(
            self: Self,
            node: Token,
            ctx: Optional[Token],
            lines: str,
            line_range: LineRange,
    ) -> None:
        self._tk = node
        self._cx = ctx

        self._line_range = line_range
        self._lines = lines

    def compile(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
