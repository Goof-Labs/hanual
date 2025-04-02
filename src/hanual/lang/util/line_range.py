from __future__ import annotations


from dataclasses import dataclass
from typing import Sequence


@dataclass()
class LineRange:
    start: int | float
    end: int | float

    def to_range(self) -> Sequence[int]:
        return range(self.start, self.end+1)
