from __future__ import annotations

from typing import Self, Generator, Optional

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.line_range import LineRange

from hanual.util import Reply, Request, Response, REQUEST_TYPE


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

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
