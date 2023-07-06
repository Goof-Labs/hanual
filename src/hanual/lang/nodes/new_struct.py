from __future__ import annotations
from hanual.compile.constant import Constant


from hanual.lang.lexer import Token
from typing import TYPE_CHECKING

from hanual.lang.nodes.base_node import BaseNode
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

    def find_priority(self) -> list[BaseNode]:
        return []

    def get_constants(self) -> list[Constant]:
        return self._args.get_constants()

    def get_names(self) -> list[str]:
        return [self._name.value, *self._args.get_names()]

    def execute(self):
        raise NotImplementedError
