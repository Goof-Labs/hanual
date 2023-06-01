from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union
from io import BytesIO


class BaseConstant(ABC):
    @abstractmethod
    def serialize(self) -> bytes:
        raise NotImplementedError

    @property
    @abstractmethod
    def value(self) -> Union[str, int]:
        raise NotImplementedError


class Int(BaseConstant):
    def __init__(self, value: int) -> None:
        self._value: int = value

    def serialize(self) -> bytes:
        return b"\x00" + self._value.to_bytes()

    @property
    def value(self) -> int:
        return self._value


class UInt(BaseConstant):
    def __init__(self, value: int) -> None:
        self._value: int = value

    def serialize(self) -> bytes:
        return b"\x01" + self._value.to_bytes()

    @property
    def value(self) -> int:
        return self._value


class Str(BaseConstant):
    def __init__(self, value: str) -> None:
        self._value: str = value

    def serialize(self) -> bytes:
        byts = BytesIO()
        byts.write(b"\x02")

        for char in self._value:
            byts.write(ord(char).to_bytes(1, byteorder="big"))

        return byts.getvalue()

    @property
    def value(self) -> str:
        return self._value


__all__ = [
    "Int",
    "UInt",
    "Str",
]
