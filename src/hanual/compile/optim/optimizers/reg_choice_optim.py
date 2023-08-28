from __future__ import annotations

from .base_optimiszer import BaseOptimizer
from hanual.compile.instruction import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager


class _RegsManager:
    def __init__(self) -> None:
        self._regs_use = {k: False for k in "ABCDE"}
        self._regs_exp = {k: False for k in "ABCDE"}
        self._regs_ali = {k: "" for k in "ABCDE"}

    @property
    def alias(self):
        return self._regs_ali

    def find_free(self, reg_name: str, instr_idx: int, _tried: bool = False):
        for name, in_use in self._regs_use.items():
            if in_use is False:
                self._regs_ali[name] = reg_name
                self._regs_use[name] = True
                return name

        if _tried:  # stop recursing infinately
            return None

        self._gc_regs(instr_idx)

        return self.find_free(reg_name, instr_idx, _tried=True)

    def find_reg(self, target: str, _tried: bool = False):
        for reg_name, val in self._regs_ali.items():
            if val == target:
                return reg_name

        return None

    def _gc_regs(self, x):
        ...


class RegChoiceOptimizer(BaseOptimizer):
    def __init__(self) -> None:
        self._appierences = {}
        self._first = False

    def make_pass(self, cm: CompileManager):
        regs = _RegsManager()

        if not self._first:
            self.make_first_pass(cm.instructions)

        for idx, instr in enumerate(cm.instructions):
            if not issubclass(type(instr), MOV):
                continue

            # if to is a reg
            if isinstance(instr.to, list):
                instr.to = regs.find_free(instr.to[0], idx)

            if isinstance(instr.val, list):
                instr.val = regs.find_reg(instr.val[0], idx)

        return cm

    def make_first_pass(self, instructions):
        """
        This will loop backwards over the instruction so we can record the last time an instruction is used.
        """
        for idx, instruction in reversed(list(enumerate(instructions))):
            if not issubclass(instruction.__class__, MOV):
                continue

            if isinstance(instruction.to, list):
                self._appierences[instruction.to[0]] = idx

            if isinstance(instruction.val, list):
                self._appierences[instruction.val[0]] = idx

    @property
    def done(self) -> bool:
        return super().done
