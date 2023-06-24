from __future__ import annotations


from typing import TypeVar, Union, Literal, Optional, List, TYPE_CHECKING
from hanual.compile.compile_manager import CompileManager
from .optimizers import *

O = TypeVar("O", bound=BaseOptimizer)


class OptimizerHandeler:
    def __init__(self, *, optimizers: Optional[List[O]] = [None]) -> None:
        self._optimizers: List[O] = [RegChoiceOptimizer()]

        # If the optimizers arg (list) starts with an elipsis ... then we extend the array
        if optimizers[0] == ...:
            self._optimizers.extend(optimizers[1:])

        elif optimizers[0]:
            self._optimizers = optimizers

    def proof_read(self, code: CompileManager):
        for optim in self._optimizers:
            optim.make_pass(code)

        return code
