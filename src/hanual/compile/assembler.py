from __future__ import annotations


from .high_level_instructions import MOV
from typing import Union
from io import StringIO


class Assembler:
    def __init__(self) -> None:
        self._external_fns = set()
        self._external_fls = set()
        self._constants = set()
        self._names = []
        self._code = []

    def add_instruction(self, i):
        self._code.append(i)

    def add_const(self, const: Union[str, int]):
        self._constants.add(const)

    def get_const_idx(self, val: Union[str, int]):
        return list(self._constants).index(val)

    def get_name_idx(self, val: Union[str, int]):
        return list(self._names).index(val)

    def add_code(self, val: Union[MOV, Any]):
        val.compile(self)

    def add_name(self, name):
        self._names.append(name)

    def find_name(self, name):
        return self._names.index(name)
