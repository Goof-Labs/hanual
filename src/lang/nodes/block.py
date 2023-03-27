from __future__ import annotations

from typing import List, Union, TypeVar
from base_node import BaseNode, ABC


T = TypeVar("T")


class CodeBlock(BaseNode, ABC):
    def __init__(self, children: Union[List[T], T]) -> None:
        self._children = children

    @property
    def children(self) -> None:
        return self._children
