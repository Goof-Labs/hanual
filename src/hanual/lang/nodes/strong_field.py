from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from hanual.compile.constants.constant import Constant

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token


# type var to represent a type in the language
T = TypeVar("T")


class StrongField(BaseNode):
    __slots__ = "_name", "_type",

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

    def execute(self, env):
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        return []

    def get_names(self) -> list[str]:
        return [self.name.value]

    def find_priority(self) -> list[BaseNode]:
        return []
