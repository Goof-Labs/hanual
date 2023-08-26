from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Union

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token

    from .f_call import FunctionCall


class IterLoop(BaseNode, ABC):
    def __init__(
            self: BaseNode,
            name: Token,
            iterator: Union[Token, FunctionCall],
    ) -> None:
        self._iterator = iterator
        self._name: Token = name

    def get_names(self) -> list[str]:
        names = [self._name.value]

        if isinstance(self._iterator, Token):
            names.append(self._iterator.value)
        else:
            names.extend(self._iterator.get_names())

        return names

    def execute(self):
        raise NotImplementedError

    def compile(self):
        raise NotImplementedError
