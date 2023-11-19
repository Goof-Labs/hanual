from __future__ import annotations

from typing import TYPE_CHECKING, Union

from hanual.lang.lexer import Token

from .base_node import BaseNode
from .strong_field import StrongField
from .strong_field_list import StrongFieldList

if TYPE_CHECKING:
    ...


class StructDefinition(BaseNode):
    __slots__ = (
        "_fields",
        "_name",
        "_lines",
        "_line_range",
    )

    def __init__(
        self: BaseNode,
        name: Token,
        fields: Union[StrongFieldList, StrongField],
        lines: str,
        line_range: int,
    ) -> None:
        # if [param:fields] is a StrongField, then we make one and add it to it
        if isinstance(fields, StrongField):
            self._fields: StrongFieldList = StrongFieldList(
                lines=lines, line_range=line_range
            ).add_field(fields)

        else:
            self._fields: StrongFieldList = fields

        self._name = name

        self._lines = lines
        self._line_range = line_range

    @property
    def raw_fields(self) -> StrongFieldList:
        return self._fields

    @property
    def fields(self) -> list[StrongField]:
        return self._fields.fields

    @property
    def name(self) -> Token:
        return self._name

    def compile(self):
        # Structs are data representation methods and need to be treated as such
        # The struct info is treated as an array (under the hood)
        raise NotImplementedError
