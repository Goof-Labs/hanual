from __future__ import annotations

from hanual.optim.optimizer_status import OptimizerStatus
from hanual.compile.instruction import *
from typing import TypeVar, Union, List
from hanual.compile.label import Label
from abc import ABC, abstractmethod

I = TypeVar("I", EXC, UPK, RET, CPY, CMP, JIF, JIT, CALL, JMP)


class BaseOptimizer(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def make_pass(
        self,
        instructions: List[Union[I, Label]],
    ) -> OptimizerStatus[List[Union[I, Label]]]:
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        raise NotImplemented
