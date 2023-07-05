from __future__ import annotations


from typing import TypeVar, TYPE_CHECKING
from hanual.compile.constant import Constant
from hanual.lang.lexer import Token
from .base_node import BaseNode
from abc import ABC


if TYPE_CHECKING:
    ...


T = TypeVar("T", bound=Token)


class FreezeNode(BaseNode, ABC):
    __slots__ = "_var"

    def __init__(self: BaseNode, var: T) -> None:
        self._var: T = var

    def compile(self) -> None:
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        return []

    def get_names(self) -> list[str]:
        return [self._var.value]

    @property
    def target(self):
        return self._var
