from __future__ import annotations

from typing import TYPE_CHECKING, Generator
from collections.abc import Iterable

from hanual.lang.nodes.base_node import BaseNode
from hanual.compile.back_end.response import Response
from hanual.compile.back_end.request import Request
from hanual.compile.back_end.reply import Reply

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from typing import Self


class Arguments[T](BaseNode):
    __slots__ = (
        "_children",
        "_lines",
        "_line_range",
    )

    def __init__(
            self,
            children: T | Iterable[T],
            lines: str = None,
            line_range: LineRange = None,
    ) -> None:
        self._children: list[T] = []
        self.add_child(children)

        self._line_range: LineRange = line_range
        self._lines: str = lines

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

    def compile(self) -> Generator[Reply | Request, Response, None]:
        ...
