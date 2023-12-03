from __future__ import annotations

from .base_instruction_parameter import BaseInstructionParameter, register


@register
class RegisterParameter(BaseInstructionParameter):
    ...
