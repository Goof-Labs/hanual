from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Tuple, Self
from enum import StrEnum, auto
from logging import warn
from io import StringIO


if TYPE_CHECKING:
    from .trace_back import TraceBack, Frame


class ErrorType(StrEnum):

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list):
        first, *others = name.split('_')
        return ''.join([first.lower(), *map(str.title, others)])

    
    cli_argument_unresolved = auto()
    non_initialized_value = auto()
    illegal_character = auto()
    keyboard_interupt = auto()
    division_by_zero = auto()
    unresolved_name = auto()
    attr_not_found = auto()
    cant_set_attr = auto()


class HanualError:
    def __init__(self,
                 pos: Tuple[int, int, int],
                 line: str,
                 name: str,
                 reason: str,
                 tb: TraceBack,
                 tip: Optional[str] = None,
                 reset_next: Optional[bool] = False) -> None:
        self._reason = reason
        self._name = name
        self._line = line
        self._tip = tip
        self._pos = pos
        self._tb = tb

        self._expect = reset_next is None # force the param to be a bool

    @property
    def expect(self) -> bool:
        return self._expect

    def add_detail(self,
                   pos: Tuple[int, int, int],
                   line: str,
                   name: str,
                   reason: str) -> None:
        if self._expect is False: # don't expect this function to be called again so warn the caller
            warn("The `add_detail` method was called twice, overwriting", stacklevel=2)

        self._pos = pos
        self._line = line
        self._reason = reason

        # we don't expect this function to be called again
        self._expect = False

    def add_frame(self, frame: Frame) -> Self:
        self._tb.add_frame(frame)
        return self

    def as_string(self) -> str:
        if self._expect: # wanted a more detailed traceback
            raise Exception("Wanted a more detailed traceback")
        
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
