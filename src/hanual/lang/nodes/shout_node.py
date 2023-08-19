from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.base_node import BaseNode

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.constant import Constant
    from hanual.lang.lexer import Token


class ShoutNode(BaseNode):
    def find_priority(self) -> list[BaseNode]:
        pass

    def __init__(self: BaseNode, shout_token: Token) -> None:
        self._st = shout_token

    @property
    def shout_token(self) -> Token:
        return self._st

    def compile(self):
        return super().compile()

    def get_constants(self) -> list[Constant]:
        return []

    def get_names(self) -> list[str]:
        return []

    def execute(self):
        raise NotImplementedError
