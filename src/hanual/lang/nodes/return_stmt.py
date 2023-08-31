from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from hanual.compile.constants.constant import Constant
from hanual.lang.builtin_lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    ...


class ReturnStatement(BaseNode, ABC):
    def __init__(self: BaseNode, value) -> None:
        self._value = value

    def compile(self) -> None:
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        if isinstance(self._value, Token):
            if self._value.type in ("STR", "INT"):
                return [Constant(self._value.value)]

        else:
            return self._value.get_constants()

    def get_names(self) -> list[str]:
        if isinstance(self._value, Token):
            if self._value.type == "ID":
                return [self._value.value]

        else:
            return self._value.get_names()

    def find_priority(self) -> list[BaseNode]:
        return []

    def execute(self, env):
        raise NotImplementedError
