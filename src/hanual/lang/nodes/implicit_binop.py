from __future__ import annotations
from hanual.compile.constant import Constant

from hanual.lang.nodes.base_node import BaseNode
from typing import Any, Dict, Union, TYPE_CHECKING
from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from .f_call import FunctionCall


class ImplicitBinop(BaseNode):
    def __init__(self: BaseNode, op: Token, right: Union[Token, FunctionCall]) -> None:
        # The left side is implied
        self._right = right
        self._op = op

    @property
    def op(self) -> Token:
        return self._op

    @property
    def right(self) -> Union[Token, FunctionCall]:
        return self._right

    def compile(self):
        return super().compile()

    def get_names(self) -> list[str]:
        if isinstance(self._right, Token):
            if self._right.type == "ID":
                return [self._right.value]

        else:
            return self._right.get_names()

    def get_constants(self) -> list[Constant]:
        if isinstance(self._right, Token):
            if self._right.type in ("STR", "NUM"):
                return [self._right.value]

        else:
            return self._right.get_constants()

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
