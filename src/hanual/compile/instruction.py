from abc import ABC, abstractmethod
from typing import TypeVar

class BaseInstruction(ABC):
    @abstractmethod
    def serialize(self):
        raise NotImplementedError

    @abstractmethod
    @property
    def load_next4(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    @property
    def load_next8(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    @property
    def operang(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return str(self)

I = TypeVar("I", bound=BaseInstruction)

class MOV(BaseInstruction):
    ...

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
