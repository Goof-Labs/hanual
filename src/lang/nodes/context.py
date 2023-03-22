from __future__ import annotations

from typing import List, Tuple, NamedTuple, Dict, Any


class VariableRef(NamedTuple):
    scope_level: int
    name: str


class Context:
    __slots__ = "_scope", "_scope_level", "_vars"

    def __init__(self) -> None:
        self._scope: List[VariableRef] = []
        self._scope_level: int = 0
        self._vars: Dict[str, Any] = {}

    def __enter__(self):
        self._scope_level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._scope_level -= 1
        self.close_scope()

    def close_scope(self):
        for i in self._scope:
            if i.scope_level >= self._scope_level:
                del self._vars[i.name]
                del i

    def is_variable(self, name: str) -> bool:
        for var in self._scope:
            if var.name == name:
                return True

        return False
