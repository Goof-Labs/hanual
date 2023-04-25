from __future__ import annotations

from typing import TypeVar, Union, List, Any, Dict
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.builtin_lexer import Token
from hanual.compile import GlobalState

T = TypeVar("T")


class Arguments(BaseNode):
    def __init__(self, children: Union[List[T], T]) -> None:

        if isinstance(children, Token):
            self._children = [children]

        elif isinstance(children, (tuple, list)):  # is itterable
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

    def compile(self, global_state: GlobalState) -> Any:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, ...]:
        return {
            "type": type(self).__name__,
            "values": [
                c.as_dict() if hasattr(c, "as_dict") else c for c in self.children
            ],
        }
