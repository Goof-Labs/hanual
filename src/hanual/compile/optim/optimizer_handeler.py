from __future__ import annotations


from hanual.compile.compile_manager import CompileManager
from .optimizers import *


class OptimizerHandler:
    def __init__(self, *, optimizers=None) -> None:

        if optimizers is None:
            optimizers = [RegChoiceOptimizer()]

        self._optimizers = optimizers

    def proof_read(self, code: CompileManager):
        for _ in range(5):
            for optim in self._optimizers:
                code = optim.make_pass(code)

        return code
