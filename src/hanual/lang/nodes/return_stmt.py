from __future__ import annotations

from abc import ABC

from typing import Dict, Any, TYPE_CHECKING
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.builtin_lexer import Token
    from hanual.compile import Assembler


class ReturnStatement(BaseNode, ABC):
    def __init__(self: BaseNode, value: Token) -> None:
        self._value: Token = value

    def compile(self, global_state: Assembler) -> Any:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return {"value": self._value}
