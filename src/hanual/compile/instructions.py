from __future__ import annotations

from enum import IntEnum


class Instruction(IntEnum):
    NOP = 0x00
    MOV = 0x01

    CMP = 0x02

    AND = 0x03
    OR = 0x04
    NOT = 0x05

    LD0 = 0x06
    LD1 = 0x07
    LD2 = 0x08
    LD3 = 0x09

    POP = 0x0A
    PSH = 0x0B

    JMP = 0x0C

    CAL = 0x0D

    RET = 0x0E
