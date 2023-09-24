from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from hanual.compile.constants.constant import Constant
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from hanual.exec.wrappers import hl_wrap
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
                yield Constant(self._value.value)

        else:
            yield from self._value.get_constants()

    def get_names(self) -> list[str]:
        if isinstance(self._value, Token):
            if self._value.type == "ID":
                return [self._value.value]

        else:
            return self._value.get_names()

    def execute(self, scope: Scope) -> Result:
        res = Result()

        if isinstance(self._value, Token):
            return hl_wrap(scope=scope, value=self._value)

        res.inherit_from(self._value.execute(scope=scope))
        return res
