from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar, Union

T = TypeVar("T")


@dataclass
class OptimizerStatus(Generic[T]):
    message: Union[str, None]
    error: str  # type of error as class
    done: bool
    code: T
