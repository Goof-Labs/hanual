from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple, Self
from enum import StrEnum, auto
from io import StringIO


if TYPE_CHECKING:
    from .trace_back import TraceBack, Frame


class ErrorType(StrEnum):

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        first, *others = name.split('_')
        return ''.join([first.lower(), *map(str.title, others)])

    cli_argument_unresolved: str = auto()
    non_initialized_value: str = auto()
    illegal_character: str = auto()
    division_by_zero: str = auto()
    unresolved_name: str = auto()
    attr_not_found: str = auto()
    cant_set_attr: str = auto()


class HanualError:
    def __init__(self,
                 pos: Optional[Tuple[int, int, int]],
                 line: Optional[str],
                 name: str,
                 reason: str,
                 tb: TraceBack,
                 tip: Optional[str] = None) -> None:
        self._reason = reason
        self._name = name
        self._line = line
        self._tip = tip
        self._pos = pos
        self._tb = tb

    def add_frame(self, frame: Frame) -> Self:
        self._tb.add_frame(frame)
        return self

    def as_string(self) -> str:
        error = StringIO()

        error.write(f"{self._name}:\n")

        for frame in self._tb.frames:
            error.write(" "+frame.summery+"\n")

        error.write("\n")
        error.write(("-"*50)+"\n")
        error.write(f"{self._pos[0]} | {self._line}")
        error.write(("-"*50)+"\n")
        error.write("\n")
        error.write(f"{self._name}: {self._reason}\n")

        if self._tip:
            error.write("tip: "+self._tip)

        return error.getvalue()
