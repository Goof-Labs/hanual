from __future__ import annotations

from hanual.compile import Instruction
from abc import ABC, abstractmethod
from typing import TypeVar, List


I = TypeVar("I", bound=Instruction)


class BasePatern(ABC):
    @abstractmethod
    def make_pass(self, instructions: List[I]) -> List[I]:
        raise NotImplementedError
