from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Union
from hanual.compile.constant import Constant

from hanual.lang.errors import Error
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
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
            self._fields: StrongFieldList = StrongFieldList().add_field(fields)

        else:
            self._fields: StrongFieldList = fields

        self._name = name

    @property
    def fields(self) -> StrongFieldList:
        return self._fields

    @property
    def name(self) -> Token:
        return self._name

    def compile(self) -> None:
        # Structs are data representation methords and need to be treated as such
        # The struct info is treated as an array (under the hood)
        return []

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def get_names(self) -> list[Constant]:
        names = []

        for field in self._fields.fields:
            names.extend(field.get_names())

        return names

    def get_constants(self) -> list[Constant]:
        consts = []

        for field in self._fields.fields:
            if isinstance(field, Token):
                consts.append(Constant(field.value))

            else:
                consts.extend(field.get_constants())

        return consts

    def find_priority(self) -> list[BaseNode]:
        return [self]

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
