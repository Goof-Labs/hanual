from __future__ import annotations
from hanual.compile.constant import Constant

from hanual.lang.builtin_lexer import Token
from typing import Dict, Any, TYPE_CHECKING

from hanual.lang.errors import Error
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    ...


class ReturnStatement(BaseNode, ABC):
    def __init__(self: BaseNode, value) -> None:
        self._value = value

    def compile(self) -> None:
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        if isinstance(self._value, Token):
            if self._value.type in ("STR", "INT"):
                return [self._value.value]

        else:
            return self._value.get_constants()

    def get_names(self) -> list[str]:
        if isinstance(self._value, Token):
            if self._value.type == "ID":
                return [self._value.value]

        else:
            return self._value.get_names()

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def as_dict(self) -> Dict[str, Any]:
        return {"value": self._value}
