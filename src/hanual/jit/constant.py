from __future__ import annotations

from typing import TypeVar, Optional, Dict, TYPE_CHECKING, Optional, Any, Generic, Union


if TYPE_CHECKING:
    from typing_extensions import Self

_T = TypeVar("_T")


class Constant(Generic[_T]):
    __slots__ = (
        "_value",
        "_atrs",
    )

    def __init__(self: Self, value: _T, atrs: Dict[str, Any] = {}) -> None:
        self._value: _T = value
        self._atrs: Dict[str, Any] = atrs

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
        if bs[0] == b"\x01":  # STR
            return cls(bs.decode())

        elif bs[0] == b"\x02":  # INT
            return cls(int.from_bytes(bs, byteorder="big"))

        elif bs[0] == b"\x03":  # FLT
            """
            A float is represented by two hole numbers, a and b. Any decimal can be expressed as
            a / b. So we dump both these numbers as 64 byte intagers like so, `A` representing a
            byte for the a constant and `B` for representing a byte from the number b. The `#`
            dentotes a padding byte so 00 in hex.

            03  #  A  A  A  A  A  A  A  A  #  B  B  B  B  B  B  B  B

            The 03 is a constant that indicates that the next bytes represent a float.
            """
            # TODO make sure that this code works

            a = int.from_bytes(bs[2:10])
            # convert the 2nd to 10th byte to an int, 64 bits
            b = int.from_bytes(bs[11:19])
            # get the 11th to 19th byte
            return cls(a / b)

        else:
            raise Exception()
