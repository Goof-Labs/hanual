from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TypeVar, Union

from hanual.compile.instruction import *
from hanual.compile.label import Label
from hanual.compile.optim.optimizer_status import OptimizerStatus

_I = TypeVar("_I", EXC, UPK, RET, CPY, CMP, JIF, JIT, CALL, JMP)


class BaseOptimizer(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def make_pass(self, instructions: List[Union[_I, Label]]) -> List[Union[_I, Label]]:
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        raise NotImplemented
