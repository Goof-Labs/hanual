from __future__ import annotations

from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.constants.constant import Constant
    from hanual.lang.lexer import Token


class ShoutNode(BaseNode):
    __slots__ = "_st", "_lines", "_line_no",

    def __init__(self: BaseNode, shout_token: Token, lines: str, line_no: int) -> None:
        self._st = shout_token

        self._line_no = line_no
        self._lines = lines

    def compile(self):
        return super().compile()

    def get_constants(self) -> list[Constant]:
        ...

    def get_names(self) -> list[str]:
        return []

    def execute(self, env):
        raise NotImplementedError
