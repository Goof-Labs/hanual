from __future__ import annotations

from typing import Self

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.line_range import LineRange
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent

class DotChain(BaseNode):
    __slots__ = ("_chain", "_lines", "_line_range")

    def __init__(self, lines: str, line_range: LineRange) -> None:
        self._chain: list[Token] = []

        self._lines = lines
        self._line_range = line_range

    def add_name(self, name: Token | DotChain) -> Self:
        if isinstance(name, Token):
            self._chain.insert(0, name)

        elif isinstance(name, DotChain):
            self._chain.extend(name.chain)

        else:
            raise Exception

        return self

    @property
    def chain(self) -> list[Token]:
        return self._chain

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
