from __future__ import annotations

from .base_ir_instr import BaseIrInstruction, takes_param


@takes_param
class LD(BaseIrInstruction):
    ...
