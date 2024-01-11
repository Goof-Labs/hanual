from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Optional

from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Request, Response, REQUEST_TYPE


if TYPE_CHECKING:
    from hanual.lang.lexer import Token


class FreezeNode[T: Token](BaseNode):
    __slots__ = "_var", "_lines", "_line_no"

    def __init__(self, var: T, lines: str, line_no: int) -> None:
        self._var: T = var

        self._line_no = line_no
        self._lines = lines

    @property
    def target(self):
        return self._var

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
