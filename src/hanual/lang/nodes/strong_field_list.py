from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, TypeVar, Self, List
from .base_node import BaseNode


T = TypeVar("T", bound=BaseNode)


class StrongFieldList(BaseNode):
    def __init__(self: BaseNode) -> None:
        self._fields: List[T] = []

    def add_field(self, field: T) -> Self:
        self._fields.append(field)
        return self

    @property
    def field(self) -> List[T]:
        return self._fields

    def compile(self) -> None:
        return super().compile()

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
