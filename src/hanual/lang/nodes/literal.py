from __future__ import asinnotations


from .base_node import BaseNode
from typing import Any
from lexer import Token



class Literal(BaseNode):
    def __init__(self: Literal, token: Token) -> None:
        self._token = token

    @property
    def value(self: Literal) -> Any:
        return self._token.value

    @property
    def position(self: Literal) -> Tuple[int, int]:
        return self._token.colm, self._token.row

    def eval(self: Literal) -> Any:
        return self.value

