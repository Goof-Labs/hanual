from .instructions import *
from enum import StrEnum
from .label import Label

"""
ABCD E
VVVV VVVV
0000 0000

A: load next 4 bytes as operang
B: load next 8 bytes as operang
C: changes heap
D: jumps to different instruction
E: the last nibble is a unique identifier
"""


class Registers(StrEnum):
    A: str = "A"
    B: str = "B"
    C: str = "C"
    D: str = "D"
    E: str = "E"
    FLG: str = "FLG"
    G: str = "G"
    FA: str = "FA"
    FP: str = "FP"
    AC: str = "AC"


"""
def mov(to, frm) -> bytes:
    instruction_bytecode = BytesIO()
    instruction_bytecode.write((0b1010_0000).to_bytes())

    # TO
    if to in map(lambda x: x.value, list(Registers)):
        instruction_bytecode.write((0b1000_0000).to_bytes())
        instruction_bytecode.write(list(Registers).index(to).to_bytes())

    elif isinstance(to, int):
        instruction_bytecode.write((0b0000_0000).to_bytes())
        instruction_bytecode.write((to).to_bytes())

    else:
        print(to)
        raise Exception

    # FROM
    if frm in list(Registers):
        instruction_bytecode.write((0b1000_0000).to_bytes())
        instruction_bytecode.write(list(Registers).index(frm).to_bytes())

    elif isinstance(frm, int):
        instruction_bytecode.write((0b0000_0000).to_bytes())
        instruction_bytecode.write((frm).to_bytes())

    else:
        raise Exception

    return instruction_bytecode.getvalue()


def call() -> bytes:
    return (0b0000_1000).to_bytes()


def make_ptr(item):
    return {}
"""


class Fragment:
    def __init__(self) -> None:
        self.export_symbols = []
        self.external_files = []
        self.external_funcs = []
        self.instructions = []
        self.indentifiers = []
        self.constants = []
        self.labels = []

    def add_const(self, const):
        if not const in self.constants:
            self.constants.append(const)

        return self.constants.index(const)

    def add_instr(self, instruction):
        self.instructions.append(instruction)

    def add_frag(self, frag):
        self.export_symbols.extend(frag.export_symbols)
        self.export_symbols = list(dict.fromkeys(self.export_symbols))

        self.external_files.extend(frag.external_files)
        self.external_files = list(dict.fromkeys(self.external_files))

        self.external_funcs.extend(frag.external_funcs)
        self.external_funcs = list(dict.fromkeys(self.external_funcs))

        self.constants.extend(frag.constants)
        self.constants = list(dict.fromkeys(self.constants))

        self.indentifiers.extend(frag.indentifiers)
        self.indentifiers = list(set(self.indentifiers))

        self.labels.extend(frag.labels)

        self.instructions.extend(frag.instructions)

    def add_external_func(self, name):
        if not name in self.external_funcs:
            self.external_funcs.append(name)

        return self.external_funcs.index(name)

    def add_name(self, name):
        if not name in self.indentifiers:
            self.indentifiers.append(name)

        return self.indentifiers.index(name)

    def add_label(self, name: str = "lost-pleb"):
        lbl = Label(name)
        self.labels.append(lbl)
        return lbl

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.export_symbols=}, {self.external_files=}, {self.external_funcs=}, {self.constants=}, {self.instructions=})"

    def __repr__(self) -> str:
        return str(self)
