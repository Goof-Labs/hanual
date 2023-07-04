from typing import Generic, TypeVar, Optional


# make IntEnum one way or another
try:
    from enum import IntEnum

except ImportError:
    from enum import Enum

    class IntEnum(int, Enum):
        ...


S = TypeVar("S")
R = TypeVar("R")


class Status(Generic[S, R]):
    def __init__(self, stat: S, res: R, code: Optional[int] = None) -> None:
        self._status = stat
        self._code = code
        self._res = res

    @property
    def status(self) -> S:
        return self._status

    @property
    def resut(self) -> R:
        return self._res

    @property
    def code(self) -> int:
        return self._code


class StatusCodes(IntEnum):
    NAME_NOT_FOUND: int = 0
