from __future__ import annotations

from typing import List, Union, TypeVar, Any
from hanual.compile import Assembler
from .base_node import BaseNode
from abc import ABC

T = TypeVar("T")


class CodeBlock(BaseNode, ABC):
    __slots__ = ("_children",)

    def __init__(self, children: Union[List[T], T]) -> None:
        if isinstance(children, (tuple, list)):  # is iterable
            self._children = [*children]

        else:  # This is just another node that we have chucked into a list
            self._children = [children]

    def add_child(self, child: CodeBlock):
        self._children.extend(child.children)
        return self

    @property
    def children(self):
        return self._children

    def compile(self, state: Assembler) -> Any:
        for child in self.children:
            child.compile(state)

    def as_dict(self) -> List[Any]:
        return [c.as_dict() if hasattr(c, "as_dict") else c for c in self.children]
