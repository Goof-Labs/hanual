from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar, Union

from hanual.lang.builtin_lexer import Token
from hanual.lang.nodes.arguments import Arguments
from hanual.lang.nodes.base_node import BaseNode

from .f_def import FunctionDefinition

if TYPE_CHECKING:
    from hanual.lang.util.line_range import LineRange

T = TypeVar("T")


class Parameters(BaseNode):
    __slots__ = (
        "_children",
        "_lines",
        "_line_no",
    )

    def __init__(
        self, children: Union[T, List[T]], lines: str, line_range: LineRange
    ) -> None:
        self._children: List[T] = []

        if isinstance(children, Token):
            self._children: List[T] = [children.value]

        elif isinstance(children, (Parameters, Arguments)):
            self._children = children.children

        elif issubclass(type(children), BaseNode):
            self._children: List[T] = [children]

        else:  # This is just another node that we have chucked into a list
            self._children: List[T] = list(children)

        self._line_range = line_range
        self._lines = lines

    def add_child(self, child):
        if isinstance(child, Parameters):
            self._children.extend(child.children)

        else:
            self._children.append(child)

        return self

    @property
    def children(self) -> List[T]:
        return self._children

    def compile(self, **kwargs):
        raise NotImplementedError
