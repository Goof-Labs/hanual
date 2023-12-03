from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar, Union

from hanual.lang.builtin_lexer import Token
from hanual.lang.nodes.base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange
    from typing import Self

T = TypeVar("T")


class Arguments(BaseNode):
    __slots__ = (
        "_children",
        "_lines",
        "_line_range",
    )

    def __init__(
            self,
            children: Union[T, List[T]],
            lines: str = None,
            line_range: LineRange = None,
    ) -> None:
        if isinstance(children, Token):
            self._children: List[T] = [children]

        elif issubclass(type(children), BaseNode):
            self._children: List[T] = [children]

        else:  # This is just another node that we have chucked into a list
            self._children: List[T] = list(*children)

        self._line_range: LineRange = line_range
        self._lines: str = lines

    def add_child(self, child) -> Self:
        if isinstance(child, Arguments):
            self._children.extend(child.children)

        else:
            self._children.append(child)

        return self

    @property
    def children(self) -> List[T]:
        return self._children

    def compile(self):
        raise NotImplementedError
