from __future__ import annotations

from typing import TYPE_CHECKING, Union

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token

    from .f_call import FunctionCall


class IterLoop(BaseNode):
    def execute(self):
        pass

    def compile(self):
        pass

    def __init__(
        self: BaseNode,
        name: Token,
        iterator: Union[Token, FunctionCall],
    ) -> None:
        self._iterator = iterator
        self._name: Token = name
