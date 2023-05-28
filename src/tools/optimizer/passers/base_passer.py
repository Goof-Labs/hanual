from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, List


I = TypeVar("I")


class BasePatern(ABC):
    @abstractmethod
    def make_pass(self, instructions: List[I]) -> List[I]:
        raise NotImplementedError
