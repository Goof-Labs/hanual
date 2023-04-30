from __future__ import annotations

from abc import ABC

from typing import TypeVar, Any, TYPE_CHECKING
from hanual.lang.lexer import Token
from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.compile import Assembler


T = TypeVar("T", bound=Token)


class FreezeNode(BaseNode, ABC):
    __slots__ = "_var"

    def __init__(self: BaseNode, var: T) -> None:
        self._var: T = var

    def compile(self, global_state: Assembler) -> Any:
        raise NotImplementedError

    @property
    def target(self):
        return self._var
