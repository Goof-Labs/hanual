from __future__ import annotations

from typing import TypeVar, Generic, TYPE_CHECKING
from hanual.lang.errors import Error


E = TypeVar("E", bound=Error)
R = TypeVar("R")


class ExecStatus(Generic[E, R]):
    ...
