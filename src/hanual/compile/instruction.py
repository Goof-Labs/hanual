from typing import Union, Optional


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
B => Stack Change
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

    NOP = 0b0000_0000

    JMP = 0b1110_0000  # unconditional Jump
    JEZ = 0b1110_0001  # Jump if 0
    JNZ = 0b1110_0010  # Jump not 0
    JIE = 0b1110_0011  # jump if error

    SWP = 0b0100_1000  # swap top two elements
    YNK = 0b1100_1100  # yank n'th element and push it to top

    PP1 = 0b0100_0000  # Pops top element
    PP2 = 0b0100_0001  # Pops two elements of stack
    PP3 = 0b0100_0010  # pops three elements of stack

    PGV = 0b1100_0000  # Push global value on stack
    PGC = 0b1100_0001  # Push constant onto stack
    PGA = 0b1100_0010  # Push global address, e.g. function

    PK2 = 0b0100_0010  # Pack top 2 elements into tuple
    PK3 = 0b0100_0011  # Pack top 3 elements into tuple
    PK4 = 0b0100_0100  # Pack top 4 elements into tuple
    PK5 = 0b0100_0101  # Pack top 5 elements into tuple
    PKN = 0b1100_1000  # Pack top n elements into tuple
    PK1 = 0b0100_1001  # Pack first value into tuple, (I forgot to add this in earlier, so now it exists)

    RZE = 0b0100_0000  # Raise Exception

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
    def stack_change(self) -> bool:
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
        return f"Instruction(opcode={InstructionEnum.get_instruction(self._opcode)!r} next={self._next})"

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
