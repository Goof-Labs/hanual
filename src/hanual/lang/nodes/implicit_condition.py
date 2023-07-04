from __future__ import annotations


from typing import Any, Dict, Union, TYPE_CHECKING
from hanual.compile.constant import Constant
from hanual.lang.errors import Error
from hanual.lang.lexer import Token
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from .f_call import FunctionCall


class ImplicitCondition(BaseNode):
    def __init__(self, op: Token, val: Union[Token, FunctionCall]) -> None:
        self._val: Union[Token, FunctionCall] = val
        self._op: Token = op

    @property
    def value(self) -> Union[Token, FunctionCall]:
        return self._val

    @property
    def op(self) -> Token:
        return self._op

    def compile(self, name: str):
        # These conditions are implicit and require the context from the parent node to
        # guess what it should compare against
        return []

    def get_constants(self) -> list[Constant]:
        if isinstance(self._val, Token):
            if self._val.type in ("STR", "NUM"):
                return [Constant(self._val.value)]

    def get_names(self) -> list[str]:
        if isinstance(self._val, Token):
            if self._val.type == "ID":
                return [Constant(self._val.value)]

        return []

    def find_priority(self):
        return []

    def execute(self):
        raise NotImplementedError
