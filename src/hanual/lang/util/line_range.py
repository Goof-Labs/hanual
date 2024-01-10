from dataclasses import dataclass


@dataclass()
class LineRange:
    start: int | float
    end: int | float
