from __future__ import annotations

from random import randbytes


class Label:
    __slots__ = "_name", "_id"

    def __init__(self, name: str, mangle: bool=False) -> None:
        self._name: str = name

        if mangle:
            self._id: str = randbytes(63).hex()
            self._name+="__"+self._id

    @property
    def name(self):
        return self._name
