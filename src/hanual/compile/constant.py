from __future__ import annotations

from typing import TypeVar, Generic, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from typing_extensions import Self

_V = TypeVar("_V")


class _TargetPlaceHolder:
    def __new__(cls) -> Self:
        raise NotImplementedError


class Constant:
    def __new__(cls, value: _V, target_cls: BaseConstant = _TargetPlaceHolder) -> Self:
        if isinstance(value, str):
            return StrConstant(value)

        elif isinstance(value, float):
            return FloatConstant(value)

        elif isinstance(value, int):
            return IntConstant(value)

        else:
            return target_cls(value)


class BaseConstant(ABC, Generic[_V]):
    def __init__(self, _value: _V) -> None:
        self._value = _value

    @property
    def value(self) -> _V:
        return self._value

    @abstractmethod
    def serialize(self) -> bytes:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{type(self).__name__}[{self.value=}]"


class StrConstant(BaseConstant):
    def serialize(self) -> bytes:
        return b"\x01" + b"\x00" + self._value.encode("ascii")


class FloatConstant(BaseConstant):
    def serialize(self) -> bytes:
        a, b = self._value.as_integer_ratio()
        return (
            b"\x03"
            + b"\x00"
            + a.to_bytes(length=8, byteorder="big")
            + b"\x00"
            + b.to_bytes(length=8, byteorder="big")
        )


class IntConstant(BaseConstant):
    def serialize(self) -> bytes:
        return b"\x02" + b"\x00" + self._value.to_bytes(length=8, byteorder="big")
