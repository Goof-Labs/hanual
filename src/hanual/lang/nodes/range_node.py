from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Generator

from .base_node import BaseNode
from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    from typing_extensions import Self

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

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
