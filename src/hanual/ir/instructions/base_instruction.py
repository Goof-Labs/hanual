from __future__ import annotations

from abc import ABC, abstractmethod
from hanual.ir.label import Label


class BaseInstruction(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


type BaseInstructionArgumentType = Label | int | str

class BaseInstructionWithArgument[BaseInstructionArgumentType](BaseInstruction):
    def __init__(self, *args, **kwargs):
        ...
