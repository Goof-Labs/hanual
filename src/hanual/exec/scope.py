from __future__ import annotations

from typing import Dict, TypeVar, Generic, Optional, Any

_H = TypeVar("_H", Any, Any)


class Scope(Generic[_H]):
    def __init__(self, parent, name: Optional[str] = "BLANK"):
        self._parent: Scope = parent
        self._env: Dict[str, _H] = {}
        self._name: str = name

    def get(self, key: str, default: Optional[Any] = None) -> _H:
        return self._env.get(key, default) or (self._parent.get(key, default=default) if self._parent else default)

    def set(self, key: str, val: _H) -> None:
        self._env[key] = val

    def extend(self, other: Dict[str, _H]):
        for k, v in other.items():
            self._env[k] = v

    # return the dict of the local scope
    def locals(self) -> Dict[str, _H]:
        return self._env

    def __str__(self) -> str:
        return f"Scope<{self._name}>\n{self._parent}"

    def __repr__(self) -> str:
        return str(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
