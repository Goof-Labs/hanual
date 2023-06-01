from __future__ import annotations

from typing import TypeVar, Union, List, Any, Dict, TYPE_CHECKING
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.builtin_lexer import Token

if TYPE_CHECKING:
    ...


T = TypeVar("T")


class Arguments(BaseNode):
    __slots__ = "_children", "_function_def"

    def __init__(self, children: Union[List[T], T]) -> None:
        self._children: List[Token, BaseNode]
        self.function_def = False

        if isinstance(children, Token):
            self._children = [children]

        elif isinstance(children, (tuple, list)):  # is iterable
            self._children = [*children]

        else:  # This is just another node that we have chucked into a list
            self._children = [children]

    def add_child(self, child):
        if isinstance(child, Arguments):
            self._children.extend(child.children)

        else:
            self._children.append(child)

        return self

    @property
    def children(self) -> List[T]:
        return self._children

    def compile(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return {
            "type": type(self).__name__,
            "values": [
                c.as_dict() if hasattr(c, "as_dict") else c for c in self.children
            ],
        }
