from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Variable:
    calue: str
    type: any
    name: str
