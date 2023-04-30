from __future__ import annotations

from typing import TypeVar, Generic, Any, Dict
from hanual.compile import Assembler
from .base_node import BaseNode

T = TypeVar("T", bound=BaseNode)
A = TypeVar("A")
B = TypeVar("B")


class AssignmentNode(BaseNode, Generic[A, B]):
    __slots__ = ("_target", "_value")

    def __init__(self: BaseNode, target: A, value: B) -> None:
        self._target: A = target
        self._value: B = value

    def compile(self, global_state: Assembler) -> Any:
        raise NotImplementedError

    @property
    def target(self) -> A:
        return self._target

    @property
    def value(self) -> B:
        return self._value

    def as_dict(self) -> Dict[str, Any]:
        return {
            "type": type(self).__name__,
            "name": self._target,
            "value": self._value.as_dict()
            if hasattr(self._value, "as_dict")
            else self._value,
        }
