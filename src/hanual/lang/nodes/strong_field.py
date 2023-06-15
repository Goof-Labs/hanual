from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, TypeVar
from hanual.compile.constant import Constant

from hanual.lang.errors import Error
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token


# typevar to represent a type in the language
T = TypeVar("T")


class StrongField(BaseNode):
    def __init__(self: BaseNode, name: Token, type_: T) -> None:
        self._name: Token = name
        self._type: T = type_

    @property
    def name(self) -> Token:
        return self._name

    @property
    def type(self) -> T:
        return self._type

    def compile(self) -> None:
        return super().compile()

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def get_constants(self) -> list[Constant]:
        return []

    def get_names(self) -> list[str]:
        return [self.name.value]

    def find_priority(self) -> list[BaseNode]:
        return []

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
