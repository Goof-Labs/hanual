from __future__ import annotations

from typing import List, Union, TypeVar
from base_node import BaseNode
from abc import ABC


T = TypeVar("T")


class CodeBlock(BaseNode, ABC):
    def eval(self: BaseNode, context) -> Any:
        pass

    def compile(self) -> Any:
        pass

    def __init__(self, children: Union[List[T], T], *nodes: Tuple[T]) -> None:
        super().__init__(*nodes)
        self._children = children

    @property
    def children(self) -> None:
        return self._children
