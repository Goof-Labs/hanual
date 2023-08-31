from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, TypeVar

from hanual.compile.constants.constant import Constant
from hanual.lang.lexer import Token

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

    def execute(self, env):
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        return []

    def get_names(self) -> list[str]:
        return [self._var.value]

    @property
    def target(self):
        return self._var
