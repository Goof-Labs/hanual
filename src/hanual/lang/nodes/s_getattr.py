from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Generator, Optional

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.lexer import Token

from hanual.util import Reply, Request, Response, REQUEST_TYPE

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class SGetattr[L: BaseNode, R: Token](BaseNode):
    __slots__ = (
        "_left",
        "_right",
        "_lines",
        "_line_range",
    )

    def __init__(self, left: L, right: R, lines: str, line_range: LineRange) -> None:
        self._left: R = right
        self._right: L = left

        self._line_range = line_range
        self._lines = lines

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
