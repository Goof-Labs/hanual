from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional

from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    ...


class BreakStatement(BaseNode, ABC):
    def execute(self):
        pass

    def __init__(self: BaseNode, node: Token, ctx: Optional[Token] = None) -> None:
        self._tk = node
        self._cx = ctx

    def compile(self) -> None:
        raise NotImplementedError
