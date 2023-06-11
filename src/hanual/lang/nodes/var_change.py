from __future__ import annotations


from typing import Any, Dict, TypeVar, TYPE_CHECKING
from hanual.compile.constant import Constant
from hanual.runtime.status import ExecStatus
from hanual.lang.errors import Error
from hanual.lang.lexer import Token
from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.runtime.runtime import RuntimeEnvironment

T = TypeVar("T", bound=BaseNode)


class VarChange(BaseNode):
    def __init__(self: BaseNode, name: Token, value) -> None:
        self._name: Token = name
        self._value: T = value

    @property
    def name(self) -> Token:
        return self._name

    @property
    def value(self) -> T:
        return self._value

    def compile(self):
        raise NotImplementedError

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def get_constants(self) -> list[Constant]:
        consts = []

        if isinstance(self._value, Token):
            if self._value.type in ("STR", "NUM"):
                consts.append(self._value.value)

        else:
            consts.extend(self._value.get_constants())

        return consts

    def get_names(self) -> list[str]:
        names = []

        names.append(self._name.value)
        names.extend(self._value.get_names())

        return names

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
