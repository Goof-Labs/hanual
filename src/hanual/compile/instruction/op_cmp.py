from __future__ import annotations

from typing import Generator, Union, Literal, NoReturn

from .base_instr import BaseInstruction
from ..instructions import Instruction


class CMP(BaseInstruction):
    def compile(self) -> Generator[bytes, None, None]:
        yield Instruction.CMP.value.to_bytes()

    def validate(self) -> Union[Literal[None], NoReturn]:
        return
