from __future__ import annotations

from typing import Generic, TYPE_CHECKING, TypeVar, Any
from hanual.exec.result import Result
from .base_value import BaseValue
from abc import ABC

if TYPE_CHECKING:
    from hanual.exec.scope import Scope

_T = TypeVar("_T")


class LiteralWrapper(BaseValue, Generic[_T], ABC):
    __slots__ = ("_value",)

    def __init__(self, value: _T) -> None:
        if isinstance(value, LiteralWrapper):
            raise Exception

        self._value = value

    def __eq__(self, other: LiteralWrapper):
        return self._value == other._value

    @property
    def value(self) -> _T:
        return self._value

    def get_attr(self, scope: Scope, attr: str) -> Result:
        raise Exception

    def as_string(self, scope: Scope) -> str:
        return str(self._value)

    def to_str(self, scope: Scope, x: Any) -> LiteralWrapper:
        return str(self._value)
