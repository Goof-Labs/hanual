from __future__ import annotations

from abc import ABC, abstractmethod
from math import log2


# The following classes only exist to outline the attributes of a class


class _Pointerable(ABC):
    # This means that pointers can exisat that point to that object

    _pointerable = True


class _Serializeable(ABC):
    # Can be serialized into a file

    @abstractmethod
    def serialize(self) -> bytes:
        raise NotImplementedError


# Data types
class String(_Pointerable, _Serializeable):
    # value is the actual value of the string
    def __init__(self, value: str) -> None:
        self._value = value


class Intager(_Pointerable, _Serializeable):
    # size is the size of our intager, e.g i32
    # value is the actual value of the intager
    def __init__(self, size: int, value: int) -> None:
        if not log2(size).is_intager():
            raise Exception(
                f"{size} is not a power of 2, i.e. not 2, 4, 8, 16, 32, ..."
            )

        self._size = size
        self._value = value


class Float(_Pointerable, _Serializeable):
    def __init__(self, val: float) -> None:
        a, b = val.as_integer_ratio()
        self.n1 = Intager(a)
        self.n2 = Intager(b)


class Array(_Pointerable, _Serializeable):
    def __init__(self) -> None:
        pass
