from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Union

from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self


class DotChain(BaseNode, ABC):
    __slots__ = ("_chain", "_lines", "_line_range")

    def __init__(self: BaseNode, lines: str, line_range: int) -> None:
        self._chain: list[Token] = []

        self._lines = lines
        self._line_range = line_range

    def add_name(self, name: Union[Token, DotChain]) -> Self:
        if isinstance(name, Token):
            self._chain.insert(0, name)

        elif isinstance(name, DotChain):
            self._chain = [*self._chain, *name.chain]

        else:
            raise Exception

        return self

    @property
    def chain(self) -> list[Token]:
        return self._chain

    def compile(self) -> None:
        raise NotImplementedError
