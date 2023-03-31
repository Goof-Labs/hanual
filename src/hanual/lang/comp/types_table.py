from enum import Enum


class TypeTable(Enum):
    # only need to worry about the last nibble, so we dont need a whole byte
    INT = 0b0000
    BOL = 0b0001
    STR = 0b0010
    CHR = 0b0011
    EXC = 0b0100
