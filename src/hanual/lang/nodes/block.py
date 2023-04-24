from __future__ import annotations

from typing import List, Union, TypeVar, Any
from hanual.compile import GlobalState
from .base_node import BaseNode
from abc import ABC

T = TypeVar("T")


class CodeBlock(BaseNode, ABC):
    __slots__ = ("_children",)

    def __init__(self, children: Union[List[T], T]) -> None:
        if isinstance(children, (tuple, list)):  # is itterable
            self._children = [*children]

        else:  # This is just another node that we have chucked into a list
            self._children = [children]

    def add_child(self, child: CodeBlock):
        self._children.extend(child.children)
        return self

    @property
    def children(self):
        return self._children

    def compile(self, global_state: GlobalState) -> Any:
        res = []

        for child in self.children:
            res.extend(child.compile(global_state))

        return res

    def as_dict(self) -> List[...]:
        return [c.as_dict() if hasattr(c, "as_dict") else c for c in self.children]
