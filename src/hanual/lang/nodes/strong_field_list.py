from __future__ import annotations

from typing import TYPE_CHECKING, List

from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self

    from .strong_field import StrongField


class StrongFieldList(BaseNode):
    __slots__ = ("_fields", "_lines", "_line_range")

    def __init__(self, lines: str, line_range: int) -> None:
        self._fields: List[StrongField] = []

        self._lines = lines
        self._line_range = line_range

    def add_field(self, field: StrongField) -> Self:
        self._fields.append(field)
        return self

    @property
    def fields(self) -> List[StrongField]:
        return self._fields

    def compile(self) -> None:
        raise NotImplementedError
