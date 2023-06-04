from typing import NamedTuple, Union
from .label import Label

"""
ABCD E
VVVV VVVV
0000 0000

A: load next 4 bytes as operang
B: load next 8 bytes as operang
C: changes heap
D: jumps to different instruction
E: the last nibble is a unique identifier
"""


class MOV(NamedTuple):
    frm: Union[str, int]
    to: Union[str, int]


class CAL(NamedTuple):
    ...


class JMP(NamedTuple):
    to: Label


class JNZ(NamedTuple):
    to: Label


class MKPTR(NamedTuple):
    of: str


class LDP(NamedTuple):
    ptr: int


class JIX(NamedTuple):
    to: Label


__all__ = ["MOV", "CAL", "JMP", "JNZ", "MKPTR", "LDP", "JIX"]
