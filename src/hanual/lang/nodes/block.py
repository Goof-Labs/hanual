from __future__ import annotations

from typing import List, Union, TypeVar, Any
from hanual.compile import GlobalState
from .base_node import BaseNode
from io import StringIO
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
        pass

    def __str__(self, level=1) -> str:
        string = StringIO()

        string.write("CodeBlock([\n".rjust(level))

        for child in self._children:
            string.write(child.__str__(level=level + 1) + "\n")

        string.write("])".rjust(level))

        return string.getvalue()
