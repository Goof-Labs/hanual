from __future__ import annotations

from random import randbytes


class Label:
    def __init__(self, name: str) -> None:
        self._name: str = name
        self._id: str = randbytes(63).hex()
