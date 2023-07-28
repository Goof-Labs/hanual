from hanual.compile.label import Label
from hanual.lang.lexer import Token
from abc import ABC, abstractmethod
from random import randbytes
from typing import Union
from io import StringIO
from .refs import Ref


class BaseInstruction(ABC):
    @abstractmethod
    def serialize(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def get_val(obj: Union[str, any]):
        if isinstance(obj, str):
            return obj

        return obj.value

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return str(self)

    # This allows for the class to have a syntax like
    # CLASSNAME[STUFF]
    # This makes it easier to distinguish class inits
    # vs instruction inits
    def __class_getitem__(cls, to):
        if to is None:
            return cls()

        return cls(*to)


class MOV(BaseInstruction, ABC):
    def __init__(self, to, val) -> None:
        self.val = val
        self.to = to

    def update(self, idx: int):
        if isinstance(self.val, Label):
            self.val.index = idx

    def __str__(self) -> str:
        return f"{type(self).__name__}[{self.to=} {self.val=}]"


"""
The following is the data for all move instructions
+--------+----------+------------+-----------+------------+------------+
|  NAME  |    TO    |   ORIGIN   |  ID (BIN) | LOAD-ARG-1 | LOAD-ARG-2 |
+--------+----------+------------+-----------+------------+------------+
| MOV_RC | register | const pool | 1110_0000 | 1 byte     | 15 bytes   |
| MOV_RR | register | register   | 1110_0001 | 1 byte     | 1 byte     |
| MOV_RF | register | reference  | 1110_0010 | 1 byte     | 7 bytes    |
| MOV_RI | register | [arg-2]    | 1110_0011 | 1 byte     | 15 bytes   |
| MOV_HH | heap     | heap       | 1110_0100 | 8 bytes    | 8 bytes    |
| MOV_HR | heap     | register   | 1110_0101 | 15 bytes   | 1 byte     |
| MOV_HF | heap     | reference  | 1110_0110 | 8 bytes    | 8 bytes    |
| MOV_HI | heap     | [arg-2]    | 1110_0111 | 8 bytes    | 8 bytes    |
| MOV_HC | heap     | constant   | 1110_1000 | 8 bytes    | 8 bytes    |
+--------+----------+------------+-----------+------------+------------+

::NOTES::
=========

NULL

"""


# move a value from the constant pool into a register
class MOV_RC(MOV):
    def serialize(self, consts: list, names: list[str], **kwargs):
        return (
            (0b1110_0000).to_bytes(length=1, byteorder="big")
            + ("ABCDEFO".index(self.to)).to_bytes(length=1, byteorder="big")
            + self.val.to_bytes(length=15, byteorder="big")
        )


# move a value from one register to another
class MOV_RR(MOV):
    def serialize(self, consts: list, names: list[str], **kwargs):
        if isinstance(self.to, str):
            to = self.to

        else:
            to = self.to.value

        if isinstance(self.val, str):
            val = self.val

        else:
            val = self.val.value

        return (
            (0b1110_0001).to_bytes(length=1, byteorder="big")
            + ("ABCDEFO".index(to)).to_bytes(length=1, byteorder="big")
            + ("ABCDEFO".index(val)).to_bytes(length=1, byteorder="big")
        )


# move a reference to a register
class MOV_RF(MOV):
    def serialize(self, names, **kwargs):
        return (
            (0b1110_0010).to_bytes(length=1, byteorder="big")
            + ("ABCDEFO".index(self.to)).to_bytes(length=1, byteorder="big")
            + names.index(self.val.ref).to_bytes(length=7, byteorder="big")
        )


# move an intager to a register
class MOV_RI(MOV):
    def serialize(self, consts: list, names: list[str], **kwargs):
        return (
            (0b1110_0011).to_bytes(length=1, byteorder="big")
            + ("ABCDEFO".index(self.get_val(self.to))).to_bytes(
                length=1, byteorder="big"
            )
            + self.val.to_bytes(length=12, byteorder="big")
        )


# move a heap value into another
class MOV_HH(MOV):
    def serialize(self, consts: list, names: list[str], **kwargs):
        return (
            (0b1110_0100).to_bytes(length=1, byteorder="big")
            + self.to.value.to_bytes(byteborder=8)
            + self.val.value.to_bytes(length=8)
        )


# move a register into the heap
class MOV_HR(MOV):
    def serialize(self, consts: list, names: list[str], **kwargs):
        return (
            (0b1110_0101).to_bytes(length=1, byteorder="big")
            + self.val.to.to_bytes(length=14, byteorder="big")
            + ("ABCDEFO".index(self.to.value)).to_bytes(length=2, byteorder="big")
        )


# move a reference into the heap
class MOV_HF(MOV):
    def serialize(self, consts: list, names: list[str], **kwargs):
        return (
            (0b1110_0110).to_bytes(length=1, byteorder="big")
            + self.to.value.to_bytes(length=14, byteorder="big"),
            +self.val.value.to_bytes(length=2, byteorder="big"),
        )


# move an int into heap
class MOV_HI(MOV):
    def serialize(self, consts: list, names: list[str], **kwargs):
        return (
            (0b1110_0111).to_bytes(length=1, byteorder="big")
            + self.to.value.to_bytes(length=8, byteorder="big")
            + self.val.value.to_bytes(length=8, byteorder="big"),
        )


# move a constant into heap
class MOV_HC(MOV):
    def serialize(self, consts: list, names: list[str], **kwargs):
        return (
            (0b1110_1000).to_bytes(length=1, byteorder="big")
            + self.to.value.to_bytes(length=8, byteorder="big")
            + self.val.value.to_bytes(length=8, byteorder="big"),
        )


class CALL(BaseInstruction):
    def __init__(self) -> None:
        ...

    def serialize(self, **kwargs):
        return (0b1000_0001).to_bytes(length=1, byteorder="big")

    def update(self):
        ...

    def __str__(self) -> str:
        return "CAL[]"


class JMP(BaseInstruction, ABC):
    def __init__(self, target):
        self._target = target

    @property
    def target(self):
        return self._target

    def serialize(self):
        return super().serialize()

    def __str__(self) -> str:
        return f"JMP[{self.target=}]"


class JIT(BaseInstruction, ABC):
    def __init__(self, target):
        self._target = target

    @property
    def target(self):
        return self._target

    def serialize(self):
        return super().serialize()

    def __str__(self) -> str:
        return f"JIT[{self.target=}]"


class JIF(BaseInstruction, ABC):
    def __init__(self, target):
        self._target = target

    @property
    def target(self):
        return self._target

    def serialize(self):
        return super().serialize()

    def __str__(self) -> str:
        return f"JIF[{self.target=}]"


class CMP(BaseInstruction, ABC):
    def __init__(self):
        ...

    def serialize(self):
        raise NotImplementedError

    def __str__(self):
        return f"CMP"


class CPY(BaseInstruction, ABC):
    def __init__(self, to, val):
        self._val = val
        self._to = to

    @property
    def val(self):
        return self._val

    @property
    def to(self):
        return self._to

    def serialize(self):
        raise NotImplementedError

    def __str__(self):
        return f"CPY[{self._to} {self._val}]"


class RET(BaseInstruction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def serialize(self, **kwargs):
        return (0b0010_0111).to_bytes(length=1, byteorder="big")

    def update(self):
        ...

    def __str__(self):
        return f"RET[{self._value}]"


class UPK(BaseInstruction):
    def __init__(self, names: list[str | Token]):
        self._names = names

    @property
    def names(self) -> list[str | Token]:
        return self._names

    def update(self):
        ...

    def serialize(self, **kwargs):
        return (0b0100_1001).to_bytes(length=1, byteorder="big")

    def __str__(self):
        val = StringIO()

        for name in self._names:
            if isinstance(name, Token):
                val.write(name.value)

            else:
                val.write(str(name))

            val.write(", ")

        return f"UPK[{val.getvalue()}]"


class EXC(BaseInstruction, ABC):
    def __init__(self, op, left, right):
        self._right = right
        self._left = left
        self._op = op

    @property
    def op(self):
        return self._op

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def serialize(self):
        raise NotImplementedError

    def __str__(self):
        return f"EXC[{self._op} {self._left} {self._right}]"


class LDC(BaseInstruction):
    def __init__(self, value: int) -> None:
        self._value = value

    @property
    def value(self):
        return self._value

    def serialize(self):
        return (0b1000_1001).to_bytes(length=1, byteorder="big") + self._value.to_bytes(
            length=8, byteorder="big"
        )

    def update(self):
        return super().update()

    def __str__(self) -> str:
        return f"LDC[{self._value}]"


def new_reg():
    return ["REG_" + randbytes(64).hex()]


def new_heap():
    return ("HEAP_" + randbytes(64).hex(),)
