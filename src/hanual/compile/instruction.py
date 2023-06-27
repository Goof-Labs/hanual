from abc import ABC, abstractmethod
from typing import TypeVar
from hanual.lang.lexer import Token
from io import StringIO
from random import randbytes


class BaseInstruction(ABC):
    @abstractmethod
    def serialize(self):
        raise NotImplementedError

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


I = TypeVar("I", bound=BaseInstruction)


class MOV(BaseInstruction):
    def __init__(self, to, val) -> None:
        self.val = val
        self.to = to

    def serialize(self):
        if isinstance(self.val, int):
            if isinstance(self.to, int):
                # addr <- addr
                ...

            elif isinstance(self.to, str):
                # reg <- addr
                ...

            else:
                raise Exception

        elif isinstance(self.to, int):
            if isinstance(self.val, int):
                # addr <- addr
                ...

            elif isinstance(self.val, str):
                # reg <- reg
                ...

            else:
                raise Exception

        else:
            raise Exception

    def __str__(self) -> str:
        return f"MOV[{self.to=} {self.val=}]"


class CALL(BaseInstruction):
    def __init__(self) -> None:
        ...

    def serialize(self):
        return super().serialize()

    def __str__(self) -> str:
        return "CAL[]"


class JMP(BaseInstruction):
    def __init__(self, target):
        self._target = target

    @property
    def target(self):
        return self._target

    def serialize(self):
        return super().serialize()

    def __str__(self) -> str:
        return f"JMP[{self.to=} {self.val=}]"


class JIT(BaseInstruction):
    def __init__(self, target):
        self._target = target

    @property
    def target(self):
        return self._target

    def serialize(self):
        return super().serialize()

    def __str__(self) -> str:
        return f"JIT[{self.to=} {self.val=}]"


class JIF(BaseInstruction):
    def __init__(self, target):
        self._target = target

    @property
    def target(self):
        return self._target

    def serialize(self):
        return super().serialize()

    def __str__(self) -> str:
        return f"JIF[{self.to=} {self.val=}]"


class CMP(BaseInstruction):
    def __init__(self):
        ...

    def serialize(self):
        raise NotImplementedError

    def __str__(self):
        return f"CMP"


class CPY(BaseInstruction):
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

    def serialize(self):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError

    def __str__(self):
        return f"RET[{self._value}]"


class UPK(BaseInstruction):
    def __init__(self, names: list[str | Token]):
        self._names = names

    @property
    def names(self) -> list[str | Token]:
        return self._names

    def serialize(self):
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


class EXC(BaseInstruction):
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
        return f"EXC[{self._op} {self._left} {self._rigth}]"


def new_reg():
    return ["REG_" + randbytes(64).hex()]


# for windcard imports
__all__ = [
    "BaseInstruction",
    "new_reg",
    "EXC",
    "UPK",
    "RET",
    "CPY",
    "MOV",
    "CMP",
    "JIF",
    "JIT",
    "CALL",
    "JMP",
]
