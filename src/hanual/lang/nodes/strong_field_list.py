from __future__ import annotations

from typing import TYPE_CHECKING, List

from hanual.compile.constants.constant import Constant

from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self

    from .strong_field import StrongField


class StrongFieldList(BaseNode):
    __slots__ = ("_fields",)

    def __init__(self) -> None:
        self._fields: List[StrongField] = []

    def add_field(self, field: StrongField) -> Self:
        self._fields.append(field)
        return self

    @property
    def fields(self) -> List[StrongField]:
        return self._fields

    def compile(self) -> None:
        raise NotImplementedError

    def execute(self, env):
        raise NotImplementedError

    def get_names(self) -> list[str]:
        names = []

        for field in self._fields:
            names.extend(field.get_names())

        return names

    def get_constants(self) -> list[Constant]:
        for field in self._fields:
            yield field.get_constants()
