from __future__ import annotations

from bytecode import Instr

from typing import Generator, Optional

from hanual.compile.context import Context
from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Response, Request, REQUEST_TYPE


class CodeBlock[C: BaseNode](BaseNode):
    __slots__ = ("_children", "_line_range", "_lines")

    def __init__(self, children: C) -> None:
        """Initializer of the CodeBlock class.

        An object that stores the children of a codeblock.
        It can have objects added to it using the `add_child` function.

        Args:
            children: The elements inside the codeblock
        """
        self._children: list[BaseNode] = []
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

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        with (yield Request[Context](Request.CREATE_CONTEXT)).response as ctx:
            ctx.add(parent=self)

            for child in self._children:
                yield from child.gen_code()

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        for child in self._children:
            yield from child.prepare()

    @property
    def children(self) -> list[BaseNode]:
        return self._children
