from __future__ import annotations

from random import randbytes


class Label:
    __slots__ = "_name", "_id", "_index"

    def __init__(self, name: str, mangle: bool = False) -> None:
        self._name: str = name
        self._index: int = 0

        if mangle:
            self._id: str = randbytes(63).hex()
            self._name += "__" + self._id

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index = val

    @property
    def name(self):
        return self._name
