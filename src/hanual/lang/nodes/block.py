from __future__ import annotations

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.util import Request


class CodeBlock(BaseNode):
    __slots__ = ("_children", "_line_range", "_lines")

    def __init__(self, children: list[BaseNode]) -> None:
        """Initializer of the CodeBlock class.

        An object that stores the children of a codeblock.
        It can have objects added to it using the `add_child` function.

        Args:
            children: The elements inside the codeblock
        """
        self._children: list[BaseNode] = []
        self.add_child(children)

    def add_child(self, child: CodeBlock | list | tuple):
        if isinstance(child, (list, tuple)):
            for child_ in child:
                self.add_child(child_)

        elif isinstance(child, CodeBlock):
            self.children.extend(child.children)

        else:
            self._children.append(child)

        return self

    def gen_code(self) -> GENCODE_RET:
        reply = yield Request(Request.CREATE_CONTEXT)

        assert reply is not None

        with reply.response as ctx:
            ctx.add(parent=self)

            for child in self._children:
                yield from child.gen_code()

    def prepare(self) -> PREPARE_RET:
        for child in self._children:
            yield from child.prepare()

    @property
    def children(self) -> list[BaseNode]:
        return self._children
