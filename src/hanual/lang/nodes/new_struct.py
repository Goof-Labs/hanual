from __future__ import annotations

from hanual.compile.constants.constant import Constant
from typing import TYPE_CHECKING, Union
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.exec.wrappers.hl_struct import HlStruct
    from hanual.lang.lexer import Token
    from .arguments import Arguments
    from .f_call import FunctionCall


class NewStruct(BaseNode):
    def __init__(self: BaseNode, call: FunctionCall) -> None:
        self._args: Arguments = call.args
        self._name: Token = call.name

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def compile(self) -> None:
        raise NotImplementedError

    def find_priority(self) -> list[BaseNode]:
        return []

    def get_constants(self) -> list[Constant]:
        return self._args.get_constants()

    def get_names(self) -> list[str]:
        return [self._name, *self._args.get_names()]

    def execute(self, scope: Scope) -> Result:
        res = Result()

        struct: Union[HlStruct, None] = scope.get(self._name.value, None)

        if struct is None:
            return res.fail(f"{self._name.value!r} was not found in scope")

        return res.success(struct.make_instance(name=struct.name, fields=struct.fields))
