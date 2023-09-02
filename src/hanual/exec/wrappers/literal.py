from __future__ import annotations

from typing import Generic, TYPE_CHECKING, TypeVar
from .base_value import BaseValue
from abc import ABC

if TYPE_CHECKING:
    from hanual.exec.scope import Scope

_T = TypeVar("_T")


class LiteralWrapper(BaseValue, Generic[_T], ABC):
    __slots__ = ("_value",)

    def __init__(self, value: _T) -> None:
        self._value = value

    @property
    def value(self) -> _T:
        return self._value

    def as_string(self, scope: Scope) -> str:
        return str(self._value)
