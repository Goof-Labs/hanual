# make IntEnum one way or another
from enum import IntEnum
from typing import Generic, Optional, TypeVar

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
