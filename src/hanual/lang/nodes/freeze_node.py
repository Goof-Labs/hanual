from __future__ import annotations

from abc import ABC

from typing import Dict, TypeVar, Any, TYPE_CHECKING
from hanual.compile.constant import Constant
from hanual.lang.errors import Error
from hanual.lang.lexer import Token
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
from .base_node import BaseNode


if TYPE_CHECKING:
    ...


T = TypeVar("T", bound=Token)


class FreezeNode(BaseNode, ABC):
    __slots__ = "_var"

    def __init__(self: BaseNode, var: T) -> None:
        self._var: T = var

    def compile(self) -> None:
        raise NotImplementedError

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def get_constants(self) -> list[Constant]:
        return []

    def get_names(self) -> list[str]:
        return [self._var.value]

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()

    @property
    def target(self):
        return self._var
