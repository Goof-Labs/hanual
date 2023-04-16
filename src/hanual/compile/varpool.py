from typing import TypeVar, Set

T = TypeVar("T")


class VarPool:
    __slots__ = ("_names",)

    def __init__(self) -> None:
        self._names: Set[T] = set()

    def add_name(self, name: T) -> None:
        self._names.add(name)

    def remove_name(self, name: T) -> None:
        self._names.remove(name)

    def exists_name(self, name: T) -> bool:
        return name in self._names
