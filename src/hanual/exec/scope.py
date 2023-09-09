from __future__ import annotations

from hanual.lang.errors import HanualError, ErrorType, TraceBack
from typing import Dict, TypeVar, Generic, Optional, Any
from hanual.exec.result import Result

_H = TypeVar("_H")


class Scope(Generic[_H]):
    def __init__(self, parent, name: Optional[str] = "BLANK"):
        self._parent: Scope = parent
        self._env: Dict[str, _H] = {}
        self._name: str = name

    def exists(self, key: str) -> bool:
        return key in self._env

    def get(self, key: str, default: Optional[Any] = None, res: Optional[bool] = False) -> _H:
        if res is False:
            return self._env.get(key, default) or (self._parent.get(key, default=default) if self._parent else default)

        val = self.get(key=key, default=None)

        if val is None:
            return Result().fail(HanualError(
                pos=None,
                line=None,
                name=ErrorType.unresolved_name,
                reason=f"Reference to {key!r} could not be resolved",
                tip="Did you make a typo?",
                tb=TraceBack()
            ))

        return Result().success(val)

    def set(self, key: str, val: _H) -> None:
        self._env[key] = val

    def extend(self, other: Dict[str, _H]):
        for k, v in other.items():
            self._env[k] = v

    # return the dict of the local scope
    def locals(self) -> Dict[str, _H]:
        return self._env

    @property
    def parent(self) -> Scope:
        return self._parent

    def __str__(self) -> str:
        return f"Scope<{self._name}>\n{self._parent!s}"

    def __repr__(self) -> str:
        return str(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
