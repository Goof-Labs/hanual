from abc import ABC, abstractmethod
from typing import TypeVar


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


I = TypeVar("I", bound=BaseInstruction)


class MOV(BaseInstruction):
    def __init__(self, to, val) -> None:
        self.val = val
        self.to = to

    @property
    def load_next4(self) -> bool:
        return super().load_next4

    @property
    def load_next8(self) -> bool:
        return super().load_next8

    @property
    def operang(self) -> bool:
        return super().operang

    @property
    def serialize(self):
        return super().serialize()

    def __str__(self) -> str:
        return f"MOV[{self.to=} {self.val=}]"

    def __class_getitem__(cls, to):
        print("HERE")
        return cls(*to)


class CALL(BaseInstruction):
    ...


class JMP(BaseInstruction):
    ...


class JIT(BaseInstruction):
    ...


class JIF(BaseInstruction):
    ...


class CMP(BaseInstruction):
    ...


class CPY(BaseInstruction):
    ...


# for windcard imports
__all__ = [
    "CPY",
    "MOV",
    "CMP",
    "JIF",
    "JIT",
    "CALL",
    "JMP",
]
