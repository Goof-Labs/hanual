from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, TypeVar, List
from hanual.compile.constant import Constant
from hanual.lang.errors import Error
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
from .base_node import BaseNode

if TYPE_CHECKING:
    from typing_extensions import Self


T = TypeVar("T", bound=BaseNode)


class StrongFieldList(BaseNode):
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

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def get_names(self) -> list[str]:
        names = []

        for field in self._fields:
            names.extend(field.get_names())

        return names

    def get_constants(self) -> list[Constant]:
        consts = []

        for field in self._field:
            consts.extend(field)

        return consts

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
