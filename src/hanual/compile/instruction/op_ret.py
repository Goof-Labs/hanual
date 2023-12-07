from __future__ import annotations

from typing import Generator, Union, Literal, NoReturn

from ..instructions import Instruction
from .base_instr import BaseInstruction, takes_param


@takes_param
class LD3(BaseInstruction):
    def compile(self) -> Generator[bytes, None, None]:
        yield Instruction.RET.value.to_bytes()

    def validate(self) -> Union[Literal[None], NoReturn]:
        return
