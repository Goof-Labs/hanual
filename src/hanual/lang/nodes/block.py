from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Generator, List, TypeVar, Union

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange

T = TypeVar("T")


class CodeBlock(BaseNode, ABC):
    __slots__ = ("_children", "_line_range", "_lines")

    def __init__(
        self, children: Union[List[T], T], lines: str, line_range: LineRange
    ) -> None:
        self._children: List[BaseNode] = []
        self.add_child(children)

        self._line_range = line_range
        self._lines = lines

    def add_child(self, child: CodeBlock):
        if isinstance(child, (list, tuple)):
            for child_ in child:
                self.add_child(child_)

        elif isinstance(child, CodeBlock):
            self.children.extend(child.children)

        else:
            self._children.append(child)

        return self

    def compile(self, cm) -> Any:
        raise NotImplementedError

    @property
    def children(self):
        return self._children
