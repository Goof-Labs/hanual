from __future__ import annotations


from typing import Any, Dict, TypeVar, TYPE_CHECKING
from hanual.compile.state_fragment import Fragment
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

    def compile(self) -> Fragment:
        raise NotImplementedError

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
