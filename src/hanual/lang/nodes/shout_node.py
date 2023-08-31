from __future__ import annotations

from typing import TYPE_CHECKING
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.constants.constant import Constant
    from hanual.lang.lexer import Token


class ShoutNode(BaseNode):
    def __init__(self: BaseNode, shout_token: Token) -> None:
        self._st = shout_token

    def find_priority(self) -> list[BaseNode]:
        return []

    def compile(self):
        return super().compile()

    def get_constants(self) -> list[Constant]:
        return []

    def get_names(self) -> list[str]:
        return []

    def execute(self, env):
        raise NotImplementedError
