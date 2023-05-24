from __future__ import annotations


from typing import Sequence, Union, Optional, TYPE_CHECKING
from .label import Label
from io import StringIO

if TYPE_CHECKING:
    from .instruction import Instruction


class Assembler:
    def __init__(self):
        self._function_table = set()
        self._file_deps = set()
        self._instructions = []
        self._fn_deps = set()
        self._labels = []
        self._index = 0
        self._heap = []

    def add_instruction(self, instruction: Instruction) -> None:
        self._instructions.append(instruction)
        self._index += 1

    def add_file_dep(self, file_name: str) -> None:
        self._file_deps.add(file_name)

    def add_function_dep(self, name: str) -> None:
        self._fn_deps.add(name)

    def add_function_rec(self, label: Label) -> None:
        self._function_table.add(label)

    def add_label(self, label: Label) -> None:
        self._labels.append(label)

    def add_to_heap(self, name: str) -> None:
        self._heap.append(name)
