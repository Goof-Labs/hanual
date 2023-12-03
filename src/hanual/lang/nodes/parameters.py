from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar
from hanual.lang.nodes.base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange

T = TypeVar("T")


class Parameters[C: BaseNode](BaseNode):
    __slots__ = (
        "_children",
        "_lines",
        "_line_no",
    )

    def __init__(
            self,
            children: (C, list[C]),
            lines: str,
            line_range: LineRange,
    ) -> None:
        self._children: list[C] = []
        self.add_child(children)

        self._line_range = line_range
        self._lines = lines

    def add_child(self, child):
        if isinstance(child, Parameters):
            self._children.extend(child.children)

        else:
            self._children.append(child)

        return self

    @property
    def children(self) -> C:
        return self._children

    def compile(self, **kwargs):
        raise NotImplementedError
