from __future__ import annotations

from hanual.lang.lexer import Token
from .base_node import BaseNode
from typing import Union, Any
from .binop import BinOpNode
from .args import Arguments


class FunctionCall(BaseNode):
    def __init__(
        self: BaseNode, name: Token, arguments: Union[Arguments, BinOpNode]
    ) -> None:
        self._args: Union[Arguments, BinOpNode] = arguments
        self._name: Token = name

    def compile(self) -> Any:
        return super().compile()

    def eval(self: BaseNode, context) -> Any:
        return super().eval(context)

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Union[Arguments, BinOpNode]:
        return self._args

    def __str__(self: FunctionCall, level=0) -> str:
        return f"{type(self).__name__}(\n{' '.rjust(level)}name = {self.name.__str__(level+1) if issubclass(type(self.name), BaseNode) else str(self.name)}\n{' '.rjust(level)}args = {self.args.__str__(level+1) if issubclass(type(self.args), BaseNode) else str(str(self.args))})\n"
