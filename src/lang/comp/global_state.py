from __future__ import annotations

from typing import Protocol, Callable, Dict, Any


class _NodeSpec(Protocol):
    getsize: Callable[[], int]


class GlobalState:
    __slots__ = "_position", "_const_pool"

    def __init__(self) -> None:
        self._position: int = 0
        self._const_pool: Dict[str, Any] = {}

    @property
    def position(self) -> int:
        return self._position

    def position_advance(self, obj: _NodeSpec) -> None:
        self._position += obj.getsize

    def get_const_val(self, name):
        if (val := self._const_pool.get(name, None)) is None:
            return val

        raise KeyError("'%s' is not a name", (val,))

    def get_const_index(self, name):
        for i, itr_name in self._const_pool:
            if itr_name == name:
                return i

        return KeyError("'%s' is not a name", (name,))
