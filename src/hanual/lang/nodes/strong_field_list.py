from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar

from hanual.compile.constants.constant import Constant

from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self


T = TypeVar("T", bound=BaseNode)


class StrongFieldList(BaseNode):
    __slots__ = "_fields",

    def __init__(self: BaseNode) -> None:
        self._fields: List[T] = []

    def add_field(self, field: T) -> Self:
        self._fields.append(field)
        return self

    @property
    def fields(self) -> List[T]:
        return self._fields

    def compile(self) -> None:
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    def get_names(self) -> list[str]:
        names = []

        for field in self._fields:
            names.extend(field.get_names())

        return names

    def get_constants(self) -> list[Constant]:
        consts = []

        for field in self._fields:
            consts.extend(field)

        return consts

    def find_priority(self):
        return []
