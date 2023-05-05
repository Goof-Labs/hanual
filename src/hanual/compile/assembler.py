from __future__ import annotations


from typing import Sequence, Union, Optional, TYPE_CHECKING
from .label import Label


if TYPE_CHECKING:
    from .instruction import Instruction


class Assembler:
    def __init__(self):
        from .stack import Stack

        self._instructions = []
        self._file_deps = set()
        self._consts = set()
        self._stk = Stack()
        self._refs = set()
        self._funcs = []
        self._index = 0

    def add_instructions(
        self, instructions: Union[Sequence[Instruction], Instruction]
    ) -> None:
        if isinstance(instructions, (tuple, list)):
            self._index += len(instructions)
            self._instructions.extend(instructions)

        else:
            self._index += 1
            self._instructions.append(instructions)

    def add_label(self, name: Optional[str] = None):
        if name is None:
            name = "lost_identity"

        label = Label(name, self._index)

        self._instructions.append(label)

        return label

    def add_constant(self, value) -> int:
        self._consts.add(value)
        return len(self._consts) - 1

    def add_file_dep(self, name):
        if isinstance(name, (list, tuple)):
            self._file_deps.update(name)

        else:
            self._file_deps.add(name)

    def add_reference(self, name):
        self._refs.add(name)

    def add_function(self, name):
        self._funcs.append(name)

    def pull_value(self, name):
        self.add_instructions(self._stk.push_item_to_top(name))

    def push_value(self, name):
        self._stk.push(name)

    @property
    def instructions(self):
        return self._instructions

    @property
    def file_deps(self):
        return self._file_deps

    @property
    def constants(self):
        return self._consts

    @property
    def refs(self):
        return self._refs
