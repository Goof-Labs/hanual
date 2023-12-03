from __future__ import annotations
from typing import TYPE_CHECKING
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from .strong_field import StrongField
    from typing_extensions import Self


class StrongFieldList[F: StrongField](BaseNode):
    __slots__ = ("_fields", "_lines", "_line_range")

    def __init__(self, lines: str, line_range: LineRange) -> None:
        self._fields: list[F] = []

        self._lines = lines
        self._line_range = line_range

    def add_field(self, field: F) -> Self:
        self._fields.append(field)
        return self

    @property
    def fields(self) -> list[F]:
        return self._fields

    def compile(self) -> None:
        raise NotImplementedError
