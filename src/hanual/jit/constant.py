from __future__ import annotations

from typing import TypeVar, OPtional, Dict, TYPE_HINTING


if TYPE_HINTING:
    from typing_extensions import Self

_T = TypeVar("_T")


class Constant:
    __slots__ = "_value", "_atrs",
    
    def __init__(self: Self, value: _T, atrs: Optional[Dict[str, Any]] = {}) -> None:
        self._value: _T = value
        self._atrs: Dict[str, Any] = atrs


    def get_value(self) -> _T:
        return self._value

    def get_attr(self, atr: str, default: Optional[Any] = None) -> Any:
        return self._atrs.get(atr, default)

    @property
    def value(self) -> _T:
        return self._value

    @property
    def atrs(self) -> Dict[str, Any]:
        return self._atrs

    @classmethod
    def from_bytes(cls, bs: bytes) -> Constant:
        if bs[0] == b"\x01":
            return

        elif bs[0] == b"\x02":
            return

        elif bs[0] == b"\x03":
            return

        elif bs[0] == b"\x04":
            return

        else:
            raise Exception()
