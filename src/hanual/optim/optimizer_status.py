from typing import Generic, TypeVar
from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class OptimizerStatus(Generic[T]):
    message: str | None
    error: str  # type of error as class
    done: bool
    code: T
