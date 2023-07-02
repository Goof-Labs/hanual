from __future__ import annotations

from enum import IntEnum


class Flags(IntEnum):
    MOV_REF = 0b0000_0001
    LOAD_CONST = 0b0000_0010
