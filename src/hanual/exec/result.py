from __future__ import annotations

from typing import Optional, TypeVar, Any, Generic, Self, Iterator

_R = TypeVar("_R", None, Any)
_E = TypeVar("_E", None, Any)


# This records the result the execution of the AST, it stores the possible error and return value
class Result(Generic[_R, _E]):
    __slots__ = "_res", "_err"

    def __init__(self, error: Optional[_E] = None, res: Optional[_R] = None) -> None:
        self._err: _E = error
        self._res: _R = res

    def success(self, res: _R) -> Self:
        self._res = res
        return self

    def fail(self, err: _E) -> Self:
        self._err = err
        return self

    def inherit_from(self, other: Result) -> Self:
        self._err = other.error
        self._res = other.response
        return self

    @property
    def response(self) -> _R:
        return self._res

    @property
    def error(self) -> _E:
        return self._err

    def __iter__(self) -> Iterator[Any]:
        return iter((self._res, self._err))
