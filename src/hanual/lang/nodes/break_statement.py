from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional

from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    ...


class BreakStatement(BaseNode, ABC):
    __slots__ = "_lines", "_line_no",

    def __init__(self: BaseNode, node: Token, ctx: Optional[Token] = None, lines: str = "", line_no: int = 0) -> None:
        self._tk = node
        self._cx = ctx

        self._line_no = line_no
        self._lines = lines

    def execute(self, env):
        raise NotImplementedError

    def compile(self) -> None:
        raise NotImplementedError
