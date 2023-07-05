from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from hanual.lang.lexer import Token
from .base_node import BaseNode

if TYPE_CHECKING:
    ...


class BreakStatement(BaseNode):
    def __init__(self: BaseNode, node: Token, ctx: Optional[Token] = None) -> None:
        self._tk = node
        self._cx = ctx

    def compile(self) -> None:
        raise NotImplementedError
