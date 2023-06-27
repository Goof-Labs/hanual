from __future__ import annotations

from typing import List, Union, TypeVar, Any, TYPE_CHECKING

from hanual.compile.constant import Constant
from hanual.lang.nodes.base_node import BaseNode
from .base_node import BaseNode
from abc import ABC

if TYPE_CHECKING:
    from hanual.lang.errors import Error

T = TypeVar("T")


class CodeBlock(BaseNode, ABC):
    __slots__ = ("_children",)

    def __init__(self, children: Union[List[T], T]) -> None:
        self._children: List[BaseNode] = []
        self.add_child(children)

    def add_child(self, child: CodeBlock):
        if isinstance(child, (list, tuple)):
            for child_ in child:
                self.add_child(child_)

        elif isinstance(child, CodeBlock):
            self.children.extend(child.children)

        else:
            self._children.append(child)

        return self

    def execute(self):
        for child in self._children:
            # If we have an error then we raise it, otherwise I just discard the return value and keep going
            err, _ = sts = child.execute(rte)

            if err:
                return sts

    def compile(self) -> Any:
        instructions = []

        for child in self.children:
            instructions.extend(child.compile())

        return instructions

    def get_constants(self) -> list[Constant]:
        lst = []

        for node in self._children:
            lst.extend(node.get_constants())

        return lst

    def get_names(self) -> list[Constant]:
        lst = []

        for node in self._children:
            lst.extend(node.get_names())

        return lst

    def find_priority(self) -> list[BaseNode]:
        priority = []

        for child in self._children:
            priority.extend(child.find_priority())

        return priority

    @property
    def children(self):
        return self._children

    def as_dict(self) -> List[Any]:
        return [c.as_dict() if hasattr(c, "as_dict") else c for c in self.children]
