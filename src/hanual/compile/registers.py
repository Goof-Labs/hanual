from __future__ import annotations

from enum import Enum


class Registers(Enum):
    A: str = "A"
    B: str = "B"
    C: str = "C"
    D: str = "D"
    E: str = "E"
    F: str = "F"
    O: str = "O"
    S: str = "O"
    R: str = "R"


class RegisterID(Enum):
    A: int = 1
    B: int = 2
    C: int = 3
    D: int = 4
    E: int = 5
    F: int = 6
    O: int = 7
