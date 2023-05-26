from __future__ import annotations

from .instruction import InstructionMVA, InstructionMVB, InstructionFLG, InstructionINT
from typing import Union, TYPE_CHECKING
from hanual.lang.lexer import Token

if TYPE_CHECKING:
    from .assembler import Assembler


class MOV:
    def __init__(
        self,
        dest: Union[Token, int, str],
        val: Union[Token, int, str],
    ) -> None:
        # dest is a name or register
        if isinstance(dest, int):
            self._dest = (dest, "H")

        else:
            self._dest = (dest, "R")

        # value
        if isinstance(val, Token):
            self._val = (val.value, "L")

        elif isinstance(val, int):
            self._val = (val, "H")

        else:
            self._val = (val, "R")

    def compile(self, cls: Assembler):
        # Heap
        if self._dest[1] == "H":
            if self._val[1] == "L":
                # literal to heap
                # FLG 0000_0000
                cls.add_instruction(InstructionFLG(0b0000_0000))
                cls.add_instruction(InstructionMVA(self._val[0]))
                cls.add_instruction(InstructionMVB(self._dest[0]))
                cls.add_instruction(InstructionINT(0x00))

            elif self._val[1] == "R":
                # Heap to register
                # FLG 0000_0001
                cls.add_instruction(InstructionFLG(0b0000_0001))
                cls.add_instruction(InstructionMVA(self._val[0]))
                cls.add_instruction(InstructionMVB(self._dest[0]))
                cls.add_instruction(InstructionINT(0x00))

            else:
                print(self._dest, self._val)
                raise Exception()

        # register
        else:
            if self._val[1] == "L":
                # lit to reg
                # FLG 0000_0010
                cls.add_instruction(InstructionFLG(0b0000_0010))
                cls.add_instruction(InstructionMVA(self._val[0]))
                cls.add_instruction(InstructionMVB(self._dest[0]))
                cls.add_instruction(InstructionINT(0x00))

            elif self._val[1] == "H":
                # reg to heap
                # FLG 0000_0011
                cls.add_instruction(InstructionFLG(0b0000_0011))
                cls.add_instruction(InstructionMVA(self._val[0]))
                cls.add_instruction(InstructionMVB(self._dest[0]))
                cls.add_instruction(InstructionINT(0x00))

            elif self._val[1] == "R":
                # reg to reg
                # FLG 0000_0100
                cls.add_instruction(InstructionFLG(0b0000_0100))
                cls.add_instruction(InstructionMVA(self._val[0]))
                cls.add_instruction(InstructionMVB(self._dest[0]))
                cls.add_instruction(InstructionINT(0x00))

            else:
                raise Exception()

    # this is syntactic suggar, MOV [A, B]
    def __class_getitem__(cls, value):
        # the intel equivilent of this is
        # mov to, from
        to, frm = value

        return cls(to, frm)
