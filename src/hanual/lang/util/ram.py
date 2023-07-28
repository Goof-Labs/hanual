from __future__ import annotations

from typing import Dict, TypeVar
from .class_getattr import ClassGetAttr


K = TypeVar("K", str, ...)
V = TypeVar("V", int, ...)


# Random Address Manager
class RAM(ClassGetAttr):
    def __class_getattr__(cls, attr):
        if cls.__instance is None:
            cls.__instance = cls()

        return getattr(cls.__instance, attr)

    def __init__(self) -> None:
        self._lists: Dict[K, V] = {}

    @property
    def lists(self) -> Dict[K, V]:
        return self._lists
