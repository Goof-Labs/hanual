from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode

from hanual.util import Reply, Response, Request


if TYPE_CHECKING:
    ...


class FreezeNode[T: Token](BaseNode):
    __slots__ = "_var", "_lines", "_line_no"

    def __init__(self, var: T, lines: str, line_no: int) -> None:
        self._var: T = var

        self._line_no = line_no
        self._lines = lines

    @property
    def target(self):
        return self._var

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
