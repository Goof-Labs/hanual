from __future__ import annotations

from bytecode import Instr

from collections.abc import Iterable
from typing import Generator, Self, Optional

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Request, Response, REQUEST_TYPE


class Arguments[T: (BaseNode, Token)](BaseNode):
    __slots__ = (
        "_children",
        "_lines",
        "_line_range",
    )

    def __init__(
        self,
        children: T | Iterable[T],
    ) -> None:
        self._children: list[T] = []
        self.add_child(children)

    def add_child(self, child) -> Self:
        if isinstance(child, Arguments):
            self._children.extend(child.children)

        elif isinstance(child, Iterable):
            self._children.extend(child)

        else:
            self._children.append(child)

        return self

    @property
    def children(self) -> list[T]:
        return self._children

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        for arg in reversed(self._children):
            yield from arg.gen_code(store=False)

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        for arg in self._children:
            yield from arg.prepare()

    def __len__(self):
        return len(self._children)
