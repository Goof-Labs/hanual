from __future__ import annotations

from typing import Generic, TypeVar, Union
from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class OptimizerStatus(Generic[T]):
    message: Union[str, None]
    error: str  # type of error as class
    done: bool
    code: T
