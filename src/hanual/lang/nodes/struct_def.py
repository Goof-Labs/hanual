from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.lexer import Token
from .base_node import BaseNode
from .strong_field import StrongField
from .strong_field_list import StrongFieldList
from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange


class StructDefinition(BaseNode):
    __slots__ = (
        "_fields",
        "_name",
        "_lines",
        "_line_range",
    )

    def __init__(
            self,
            name: Token,
            fields: StrongFieldList | StrongField,
            lines: str,
            line_range: LineRange,
    ) -> None:
        # if [param:fields] is a StrongField, then we make one and add it to it
        if isinstance(fields, StrongField):
            self._fields: StrongFieldList = StrongFieldList(lines=lines, line_range=line_range)
            self._fields.add_field(fields)

        else:
            self._fields: StrongFieldList = fields  # type: ignore

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

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
