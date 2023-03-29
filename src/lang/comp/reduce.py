from __future__ import annotations


class Reducer:
    def __init__(self) -> None:
        self._divisions = {}
        self._const_pool = {}

    def compile_frag(self):
        ...

    @property
    def divisions(self):
        return self._divisions

    @property
    def const_pool(self):
        return self._const_pool
