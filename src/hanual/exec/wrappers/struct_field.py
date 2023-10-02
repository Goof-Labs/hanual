from __future__ import annotations

from typing import Optional, Generic, TypeVar

_T = TypeVar("_T")


class HlStructField(Generic[_T]):
    __slots__ = "_value", "_private",
    
    def __init__(self, val: _T, private: Optional[bool] = False) -> None:
        self._private = private
        self._value = val

    @property
    def value(self) -> _T:
        if self._private:
            raise Exception("Can't get provate method, use `raw_val_get` instead")
        return self._value
