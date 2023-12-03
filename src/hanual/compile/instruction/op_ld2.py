from __future__ import annotations

from typing import Generator, Union, Literal, NoReturn

from ..instruction_parameter.register_parameter import RegisterParameter
from ..instructions import Instruction
from .base_instr import BaseInstruction, takes_param


@takes_param
class LD2(BaseInstruction):
    def compile(self) -> Generator[bytes, None, None]:
        yield Instruction.LD2.value.to_bytes()

    def validate(self) -> Union[Literal[None], NoReturn]:
        assert isinstance(self._params[0], RegisterParameter)
        return
