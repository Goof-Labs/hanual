from __future__ import annotations

from typing import TypeVar, Generic


T = TypeVar("T")


class A(Generic[T]):
    def __init__(self) -> None:
        print(type(T))

    @property
    def x(self):
        ...


print(A().x["abc"]())
