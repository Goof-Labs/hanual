from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, TypeVar

from hanual.lang.errors import Error
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token


# typevar to represent a type in the language
T = TypeVar("T")


class StrongField(BaseNode):
    def __init__(self: BaseNode, name: str, type_: T) -> None:
        self._name: str = name
        self._type: T = type_

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> T:
        return self._type

    def compile(self) -> None:
        return super().compile()

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
