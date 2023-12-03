from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum


class ParameterType(IntEnum):
    ADDR = 0x01
    REGISTER = 0x02


class RegisterType(IntEnum):
    R0 = 0x00
    R1 = 0x01
    R2 = 0x02
    R3 = 0x03


def address[C: BaseInstructionParameter](cls: C) -> C:
    assert hasattr(cls, "_store_type"), f"{type(cls).__name__!r} must have a `_store_type` attr"
    cls._store_type = ParameterType.ADDR
    return cls


def register[C: BaseInstructionParameter](cls: C) -> C:
    assert hasattr(cls, "_store_type"), f"{type(cls).__name__!r} must have a `_store_type` attr"
    cls._store_type = ParameterType.REGISTER
    return cls


class BaseInstructionParameter[T](ABC):
    def __init__(self, value: T):
        raise NotImplementedError

    @abstractmethod
    def as_bytes(self) -> bytes:
        raise NotImplementedError
