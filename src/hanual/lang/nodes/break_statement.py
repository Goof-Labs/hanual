from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING
from hanual.lang.lexer import Token
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile import Assembler


class BreakStatement(BaseNode):
    def __init__(self: BaseNode, node: Token, ctx: Optional[Token] = None) -> None:
        self._tk = node
        self._cx = ctx

    def compile(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return {"type": "break", "ctx": self._cx}
