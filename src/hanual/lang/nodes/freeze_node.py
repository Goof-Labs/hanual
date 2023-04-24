from __future__ import annotations

from abc import ABC

from hanual.compile import GlobalState
from hanual.lang.lexer import Token
from .base_node import BaseNode
from typing import TypeVar, Any


T = TypeVar("T", bound=Token)


class FreezeNode(BaseNode, ABC):
    __slots__ = "_var"

    def __init__(self: BaseNode, var: T) -> None:
        self._var: T = var

    def compile(self, global_state: GlobalState) -> Any:
        return super().compile(global_state)

    @property
    def target(self):
        return self._var
