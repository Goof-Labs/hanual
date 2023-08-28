from __future__ import annotations

from typing import TYPE_CHECKING, List, Union
from hanual.lang.lexer import Token
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from typing_extensions import Self


class DotChain(BaseNode, ABC):
    __slots__ = "_chain",

    def __init__(self: BaseNode) -> None:
        self._chain: List[Token] = []

    def add_name(self, name: Union[Token, DotChain]) -> Self:
        if isinstance(name, Token):
            self._chain.insert(0, name)

        elif isinstance(name, DotChain):
            self._chain = [*self._chain, *name.chain]

        else:
            raise Exception

        return self

    @property
    def chain(self) -> List[Token]:
        return self._chain

    def compile(self) -> None:
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError
