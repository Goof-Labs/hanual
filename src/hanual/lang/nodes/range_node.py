from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Self

from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

from .base_node import BaseNode

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

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
