from __future__ import annotations

from .instructions import InstructionMOV
from typing import TYPE_CHECKING, Union, List

if TYPE_CHECKING:
    from .constants import UInt, Int, Str


class IR:
    def __init__(self) -> None:
        self._constants: List[Union[UInt, Int, Str]] = []
        self._instructions = []
        self._cell_count = 0
        self._labels = []

    def add_const(self, const: Union[UInt, Int, Str]):
        if idx := self.get_const(const):
            return idx

        self._constants.append(const)
        return len(self._constants)

    def get_const(self, const: Union[UInt, Int, Str]):
        try:
            if const.value in (lst := map(lambda x: x.value, self._constants)):
                return list(lst).index(const.value)

        except IndexError:
            return None

    def move(self, to, frm):
        self._instructions.append(InstructionMOV(to, frm))

    def get_mem_ref(self):
        self._cell_count += 1
        return self._cell_count - 1

    def free_mem_ref(self, ref):
        ...
