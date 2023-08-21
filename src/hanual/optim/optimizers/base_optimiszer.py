from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TypeVar, Union

from hanual.compile.instruction import *
from hanual.compile.label import Label
from hanual.optim.optimizer_status import OptimizerStatus

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
