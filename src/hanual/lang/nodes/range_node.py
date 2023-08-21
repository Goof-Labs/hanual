from __future__ import annotations

from abc import ABCMeta
from typing import TYPE_CHECKING, Optional

from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self

    from hanual.lang.lexer import Token


class RangeNode(BaseNode, metaclass=ABCMeta):
    def execute(self):
        pass

    def __init__(
        self: Self,
        from_: Optional[Token] = None,
        to_: Optional[Token] = None,
    ) -> None:
        self._from = from_
        self._to = to_

    def compile(self) -> None:
        raise NotImplementedError
