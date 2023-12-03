from __future__ import annotations

from typing import Generator

from ..instruction_parameter import RegisterParameter
from .base_instr import BaseInstruction, takes_param
from ..instructions import Instruction


@takes_param(2)
class MOV(BaseInstruction):
    def validate(self):
        assert len(self._params) == 0
        assert isinstance(type(self._params[0]), RegisterParameter)
        assert isinstance(type(self._params[1]), RegisterParameter)

    def compile(self) -> Generator[bytes, None, None]:
        yield Instruction.MOV.value.to_bytes()

        yield self._params[0].as_bytes()
        yield self._params[1].as_bytes()
