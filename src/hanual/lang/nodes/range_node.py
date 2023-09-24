from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from typing_extensions import Self
    from hanual.lang.lexer import Token


class RangeNode(BaseNode, ABC):
    __slots__ = "_from", "_to", "_lines", "_line_no",

    def __init__(
            self: Self,
            from_: Optional[Token] = None,
            to_: Optional[Token] = None,
            lines: str = "",
            line_no: int = 0
    ) -> None:
        self._from = from_
        self._to = to_

        self._line_no = line_no
        self._lines = lines

    def execute(self, env):
        raise NotImplementedError

    def compile(self) -> None:
        raise NotImplementedError
