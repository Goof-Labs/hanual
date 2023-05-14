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

    def add_label(
        self,
        name: Optional[str] = None,
        *,  # force programmer to specifiy the keyword args
        add_now: bool = False,
        label: Optional[Label] = None,
    ):
        """
        Add label will take in one of the following:
        A => name
        B => name , add_now
        C => label

        A =>
        This will take only the name, this creates a label and will add it to the instructions
        imidiately, it will also return the label object.

        B =>
        This will create a label but not add it, this must be done manually by the programer,
        this will be usefull if the label needs to be added later, in this case the method name
        is somewhat missleading, but the programmer must uyse the keywords so I guess it
        balances out.

        C =>
        This will just add the label to the instructions, this only exists because it fits the
        method's name well, as aposed to `add_raw_label`.
        """

        if isinstance(label, Label):
            self._instructions.append(label)
            return

        if name is None:
            name = "lost_identity"

        label = Label(name, self._index)

        if add_now:
            self._instructions.append(label)

        return label

    def add_constant(self, value) -> int:
        self._consts.add(value)

        return list(self._consts).index(value)

    def add_file_dep(self, name):
        if isinstance(name, (list, tuple)):
            self._file_deps.update(name)

        else:
            self._file_deps.add(name)

    def add_reference(self, name):
        self._refs.add(name)
        return list(self._refs).index(name)

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
