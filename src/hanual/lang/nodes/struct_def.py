from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Union
from .strong_field_list import StrongFieldList
from .strong_field import StrongField
from hanual.lang.lexer import Token
from .base_node import BaseNode


if TYPE_CHECKING:
    ...


class StructDefinition(BaseNode):
    def __init__(
        self: BaseNode,
        name: Token,
        fields: Union[StrongFieldList, StrongField],
    ) -> None:
        # if [param:fields] is a StrongField then we make one and add it to it
        if isinstance(fields, StrongField):
            self._fields = StrongFieldList().add_field(fields)

        else:
            self._fields = fields

        self._name = name

    @property
    def fields(self) -> StrongFieldList:
        return self._fields

    @property
    def name(self) -> Token:
        return self._name

    def compile(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
