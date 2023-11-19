from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional

from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self

    from hanual.lang.util.line_range import LineRange


class BreakStatement(BaseNode, ABC):
    __slots__ = (
        "_lines",
        "_line_range",
    )

    def __init__(
        self: Self,
        node: Token,
        ctx: Optional[Token] = None,
        lines: str = "",
        line_range: LineRange = 0,
    ) -> None:
        self._tk = node
        self._cx = ctx

        self._line_range = line_range
        self._lines = lines

    def compile(self) -> None:
        raise NotImplementedError
