from __future__ import annotations


from typing import Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .instructions import *

"""
Each instruction is a byte so thare are a possible of 256 possible instructions.
The Instruction set can be devided into two catagories, ones which require an
operan aka argument. And ones which dont require one. By using some bit fiddeling
we can have the most significant byte, first bit, be like a flag where a 1
represents it requiring a second operator and a 0 is no nest operator required.

ABCD
vvvv
0000 0000
    |----|
This part is to separate the starting arguments from indevidual operators unless
specified otherwise.


A => The most significant bit indecates if the next byte should be loaded as an operang.
B => Heap Change
C => Hop, if we are hopping to another instruction
D => Reserved, set to 0
"""


class InstructionEnum:
    @staticmethod
    def get_instruction(value: int):
        for name in dir(InstructionEnum):
            if name.startswith("__"):
                continue

            item: int = getattr(InstructionEnum, name)

            if not isinstance(item, int):
                continue

            if item == value:
                return name

    NOP = 0b0000_0000  # NO OP

    JMP = 0b1010_0000  # unconditional Jump
    JEZ = 0b1010_0001  # Jump if 0
    JNZ = 0b1010_0010  # Jump not 0
    JIE = 0b1010_0011  # jump if error

    LDC = 0b1100_0000
    FPA = 0b1000_0000  # Func Pointer Asignment, will take a function pointer from heap and put in register, FP
    CFA = 0b0000_0001  # Clear Function Args

    # may use flag to indicate if from const pool instead
    AFA = 0b1000_0010  # Add Function Arguments, load a value of heap and add to the function arguments

    MVA = 0b1000_0001  # move into registers ABCDE
    MVB = 0b1000_0100
    MVB = 0b1000_0101
    MVC = 0b1000_0110
    MVD = 0b1000_0111
    MVE = 0b1000_1000
    MVG = 0b1000_1001  # move into status

    FLG = 0b1000_0011  # move a byte from A register into Flag register

    RZE = 0b0010_0000  # Raise Exception

    INT = 0b1000_1111  # Interupt

    CAL = 0b0100_0001  # Call function
    RET = 0b0000_0001  # return


class InstructionInfo:
    def __init__(self, opcode: int, argument: Optional[int] = None):
        self._opcode = opcode

        self._next: int = argument

    @property
    def has_operang(self) -> bool:
        # most significant bit
        return self._opcode & 1 != 0

    @property
    def heap_change(self) -> bool:
        # 7th bit
        return self._opcode & 7 != 0

    @property
    def can_jump(self) -> bool:
        # 6th bit
        return self._opcode & 6 != 0

    @property
    def id(self) -> bool:
        # 7th bit
        return self._opcode & 0x0F != 0


class Instruction(InstructionInfo):
    def __init__(self, opcode: int, argument: Union[int, None] = None):
        super().__init__(opcode, argument)

    def __repr__(self) -> str:
        return f"Instruction(opcode={InstructionEnum.get_instruction(self._opcode)!r}, next={self._next})"

    def as_bytes(self):
        if not self._next:
            return self._opcode

        return (self._opcode << 8) | self._next

    @property
    def opcode(self):
        return self._opcode

    @property
    def next(self):
        if self._next is not None:  # We must do this, the next could be a 0
            return self._next

        return None


def _constructor_with_arg(self, opcode: int):
    super(Instruction, self).__init__(self.inst, opcode)


def _constructor_no_arg(self):
    super(Instruction, self).__init__(self.inst)


for name in dir(InstructionEnum):
    if "_" in name:
        continue

    # get the instruction byte e.g byte to repr a NOP
    inst = getattr(InstructionEnum, name)

    if inst & 1 != 0:  # has an argument
        constructor = _constructor_with_arg
    else:
        constructor = _constructor_no_arg

    tmp = type(
        f"Instruction{name}",
        (Instruction,),
        {
            "__init__": constructor,
            "inst": inst,
        },
    )

    exec(f"Instruction{name} = tmp")
