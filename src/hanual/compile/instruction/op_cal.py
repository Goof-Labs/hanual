from __future__ import annotations

from typing import Generator, Union, Literal, NoReturn

from ..instruction_parameter.address_parameter import AddressParameter
from .base_instr import BaseInstruction, takes_param
from ..instructions import Instruction


@takes_param
class CAL(BaseInstruction):
    def compile(self) -> Generator[bytes, None, None]:
        yield Instruction.CAL.value.to_bytes()

    def validate(self) -> Union[Literal[None], NoReturn]:
        assert isinstance(self._params[0], AddressParameter)
        return
