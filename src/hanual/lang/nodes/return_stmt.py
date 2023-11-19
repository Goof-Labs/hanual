from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class ReturnStatement(BaseNode, ABC):
    __slots__ = (
        "_value",
        "_lines",
        "_line_range",
    )

    def __init__(self: BaseNode, value, lines: str, line_range: LineRange) -> None:
        self._value = value

        self._line_range = line_range
        self._lines = lines

    def compile(self) -> None:
        raise NotImplementedError
