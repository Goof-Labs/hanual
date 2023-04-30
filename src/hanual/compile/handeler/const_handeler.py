from __future__ import annotations


class ConstantHandeler:
    def __init__(self, cls) -> None:
        self._cls = cls

    def add_const(self, value) -> int:
        self._cls.const_pool.append(value)
        return len(self._cls.const_pool) - 1
