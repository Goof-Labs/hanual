from __future__ import annotations

from typing import Any, Dict, Union, TYPE_CHECKING
from hanual.compile.constant import Constant

from hanual.lang.errors import Error
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
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

    def compile(self):
        return super().compile()

    def get_constants(self) -> list[Constant]:
        if isinstance(self._val, Token):
            if self._val.type in ("STR", "NUM"):
                return [self._val.value]

    def get_names(self) -> list[str]:
        if isinstance(self._val, Token):
            if self._val.type == "ID":
                return [self._val.value]

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
