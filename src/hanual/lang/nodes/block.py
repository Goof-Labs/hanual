from __future__ import annotations

from typing import TYPE_CHECKING, Generator
from abc import ABC

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.back_end.response import Response
    from hanual.compile.back_end.reply import Reply
    from hanual.lang.util.line_range import LineRange


class CodeBlock[C: BaseNode](BaseNode, ABC):
    __slots__ = ("_children", "_line_range", "_lines")

    def __init__(self, children: C, lines: str, line_range: LineRange) -> None:
        """Initializer of the CodeBlock class.

        An object that stores the children of a codeblock.
        It can have objects added to it using the `add_child` function.

        Args:
            children: The elements inside the codeblock
            lines: The lines of the code that comprises the code block
            line_range: Range of line the codeblock takes up
        """
        self._children: list[BaseNode] = []
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

    def compile(self) -> Generator[Reply, Response, None]:
        for child in self._children:
            yield from child.compile()

    @property
    def children(self):
        return self._children
