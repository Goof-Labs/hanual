from __future__ import annotations

from typing import TYPE_CHECKING, Union

from hanual.compile.constants.constant import Constant
from hanual.exec.result import Result
from hanual.lang.lexer import Token

from .base_node import BaseNode
from .strong_field import StrongField
from .strong_field_list import StrongFieldList

if TYPE_CHECKING:
    from hanual.exec.scope import Scope


class StructDefinition(BaseNode):
    def __init__(
        self: BaseNode,
        name: Token,
        fields: Union[StrongFieldList, StrongField],
    ) -> None:
        # if [param:fields] is a StrongField, then we make one and add it to it
        if isinstance(fields, StrongField):
            self._fields: StrongFieldList = StrongFieldList().add_field(fields)

        else:
            self._fields: StrongFieldList = fields

        self._name = name

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
        return []

    def execute(self, scope: Scope) -> Result:
        from hanual.exec.wrappers import HlStruct

        scope.set(self.name.value, HlStruct(self))
        return Result().success(None)

    def get_names(self) -> list[Constant]:
        for field in self._fields.fields:
            yield from field.get_names()

    def get_constants(self) -> list[Constant]:
        for field in self._fields.fields:
            if isinstance(field, Token):
                yield Constant(field.value)

            else:
                yield from field.get_constants()
