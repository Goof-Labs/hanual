from __future__ import annotations


from typing import Optional, TYPE_CHECKING
from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from typing_extensions import Self


class RangeNode(BaseNode):
    def __init__(
        self: Self,
        from_: Optional[Token] = None,
        to_: Optional[Token] = None,
    ) -> None:
        self._from = from_
        self._to = to_

    def compile(self) -> None:
        raise NotImplementedError
