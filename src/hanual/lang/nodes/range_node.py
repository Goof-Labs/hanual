from __future__ import annotations

from bytecode import Instr

from typing import TYPE_CHECKING, Optional, Generator, Self

from .base_node import BaseNode
from hanual.util import Reply, Request, Response, REQUEST_TYPE

if TYPE_CHECKING:
    from hanual.lang.lexer import Token


class RangeNode(BaseNode):
    __slots__ = (
        "_from",
        "_to",
        "_lines",
        "_line_no",
    )

    def __init__(
        self: Self,
        from_: Optional[Token] = None,
        to_: Optional[Token] = None,
        lines: str = "",
        line_no: int = 0,
    ) -> None:
        self._from = from_
        self._to = to_

        self._line_no = line_no
        self._lines = lines

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        raise NotImplementedError

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        raise NotImplementedError
