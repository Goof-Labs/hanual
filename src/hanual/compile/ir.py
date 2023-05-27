from __future__ import annotations


from .jump import Jump, ConditionalJump
from .comparisons import Cmp
from .basics import Call
from .label import Label
from typing import Self
from .mem import Move


class IR:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        self.instructions = []
        self.constants = []
        self.labels = []
        self.names = []
        self.regs = {k: False for k in ("A", "B", "C", "D", "E")}
        self.idx = 0

    def label(self, name: str) -> Label:
        # add a label
        label = Label(name, idx=self.idx)
        self.labels.append(label)
        return label

    def mov(self, to, val) -> None:
        self.instructions.append(Move(to, val))
        self.idx += 1

    def jmp(self, to: Label):
        self.instructions.append(Jump(to))
        self.idx += 1

    def cjmp(self, to: Label):
        self.instructions.append(ConditionalJump(to))
        self.idx += 1

    def cmp(self, left, right, op):
        self.instructions.append(Cmp(left, right, op))
        self.idx += 1

    def call(self):
        self.instructions.append(Call())
        self.idx += 1

    def reg_name(self, name: str):
        self.names.append(name)
        return self.find_name(name)

    def find_name(self, name: str):
        return self.names.index(name)

    def reserve_reg(self) -> str:
        # found is None U [A FREE REGISTER]
        found = None

        for k, v in self.regs.items():
            if not v:
                # or register is not reserved
                found = k

        if found:
            return found

        else:
            raise Exception("No free registers")

    def free_reg(self, k):
        if not (k in self.regs.keys()):
            raise Exception(f"{k!r} is not a register")

        self.regs[k] = False
