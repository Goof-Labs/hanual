from __future__ import annotations

from typing import TypeVar, Generic, TYPE_CHECKING, Union
from hanual.lang.errors import Error


E = TypeVar("E", bound=Error)
R = TypeVar("R")


class ExecStatus(Generic[E, R]):
    def __init__(self, error: E, result: R) -> None:
        self._error: Union[E, None] = error
        self._res: Union[R, None] = result

    @property
    def error(self) -> E:
        return self._error

    @property
    def result(self) -> R:
        return self._res

    def __iter__(self):
        return iter((self._error, self._res))
