from __future__ import annotations

from typing import List, Union, TypeVar, Any, TYPE_CHECKING
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from hanual.compile import Assembler

T = TypeVar("T")


class CodeBlock(BaseNode, ABC):
    __slots__ = ("_children",)

    def __init__(self, children: Union[List[T], T]) -> None:
        self._children = []
        self.add_child(children)

    def add_child(self, child: CodeBlock):
        if isinstance(child, (list, tuple)):
            if isinstance(child[0], str):
                self._children.append(child[1])

            else:
                self._children.extend(child)

        else:
            self._children.append(child)

        return self

    @property
    def children(self):
        return self._children

    def compile(self, state: Assembler) -> Any:
        for child in self.children:
            child.compile(state)

    def as_dict(self) -> List[Any]:
        return [c.as_dict() if hasattr(c, "as_dict") else c for c in self.children]
