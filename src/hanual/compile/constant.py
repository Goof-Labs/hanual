from __future__ import annotations

from typing import TypeVar, Generic, Any, Optional
from abc import ABC, abstractmethod

_V = TypeVar("_V")


class Constant:
    def __new__(
        cls, value: _V, default: Optional[_C] = None
    ) -> StrConstant[str] | FloatConstant[float] | IntConstant[int] | Any:
        if default is not None:
            if callable(default):
                return default(value)

            else:
                raise Warning(
                    f"{type(default).__name__} is not callable, falling back to generic constants"
                )

        if isinstance(value, str):
            return StrConstant(value)

        elif isinstance(value, float):
            return FloatConstant(value)

        elif isinstance(value, int):
            return IntConstant(value)

        else:
            raise AttributeError(
                f"{value!r} was not of type str|float|int, if a warning was given make the default callable"
            )


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
        return f"{type(self).__name__}[value={self.value!r}]"


_C = TypeVar("_C", bound=BaseConstant)


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
