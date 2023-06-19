from abc import ABC, abstractmethod
from typing import TypeVar
from hanual.lang.lexer import Token
from io import StringIO
from random import randbytes

class BaseInstruction(ABC):
    @abstractmethod
    def serialize(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def load_next4(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def load_next8(self) -> bool:
        raise NotImplementedError

    @property
    @abstractmethod
    def operang(self) -> bool:
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
        return cls(*to)


I = TypeVar("I", bound=BaseInstruction)


class MOV(BaseInstruction):
    def __init__(self, to, val) -> None:
        self.val = val
        self.to = to

    @property
    def load_next4(self) -> bool:
        return False

    @property
    def load_next8(self) -> bool:
        return True

    @property
    def operang(self) -> bool:
        return f"{self.val} {self.to}"

    def serialize(self):
        return super().serialize()

    def __str__(self) -> str:
        return f"MOV[{self.to=} {self.val=}]"

class CALL(BaseInstruction):
    ...


class JMP(BaseInstruction):
    ...


class JIT(BaseInstruction):
    def __init__(self, target):
        self._target = target

    @property
    def target(self):
        return self._target

    @property
    def load_next4(self):
        return False

    @property
    def load_next8(self):
        return True

    @property
    def operang(self) -> bool:
        return self.target

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

    @property
    def load_next4(self):
        return False

    @property
    def load_next8(self):
        return True

    @property
    def operang(self) -> bool:
        return self.target

    def serialize(self):
        return super().serialize()

    def __str__(self) -> str:
        return f"JIF[{self.to=} {self.val=}]"


class CMP(BaseInstruction):
    ...


class CPY(BaseInstruction):
    ...


class RET(BaseInstruction):
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value

    @property
    def load_next4(self):
        return False

    @property
    def load_next8(self):
        return True
    
    def serialize(self):
        raise NotImplementedError

    @property
    def operang(self):
        return self._value

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

    @property
    def load_next4(self) -> bool:
        return False

    @property
    def load_next8(self) -> bool:
        return False

    def serialize(self):
        raise NotImplementedError

    @property
    def operang(self):
        return self._names

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

    @property
    def load_next4(self) -> bool:
        return False

    @property
    def load_next8(self) -> bool:
        return True

    def serialize(self):
        raise NotImplementedError

    @property
    def operang(self):
        return self._names

    def __str__(self):
        return f"EXC[{self._op} {self._left} {self._rigth}]"

def new_reg():
    return ["REG_"+randbytes(64).hex()]

# for windcard imports
__all__ = [
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
