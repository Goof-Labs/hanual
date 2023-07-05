from __future__ import annotations


from hanual.lang.lexer import Token
from typing import TYPE_CHECKING
from .base_node import BaseNode


if TYPE_CHECKING:
    from .arguments import Arguments
    from .f_call import FunctionCall


class NewStruct(BaseNode):
    def __init__(self: BaseNode, call: FunctionCall) -> None:
        self._args: Arguments = call.args
        self._name: Token = call.name

    @property
    def name(self) -> FunctionCall:
        return self._name

    @property
    def args(self) -> FunctionCall:
        return self._args

    def compile(self) -> None:
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
