from __future__ import annotations


from typing import TYPE_CHECKING, Any, Dict
from hanual.lang.errors import Error
from hanual.lang.lexer import Token


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

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
