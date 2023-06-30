from __future__ import annotations

from enum import StrEnum, IntEnum


class Registers(StrEnum):
    A: str = "A"
    B: str = "B"
    C: str = "C"
    D: str = "D"
    E: str = "E"
    F: str = "F"
    O: str = "O"

class RegisterID(IntEnum):
    A: int = 1
    B: int = 2
    C: int = 3
    D: int = 4
    E: int = 5
    F: int = 6
    O: int = 7
