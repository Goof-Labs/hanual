from __future__ import annotations

from typing import NewType, TypeVar, Union, List
from nodes.base_node import BaseNode
from io import BytesIO


Node = TypeVar("Node", bound=BaseNode)


class Compiler:
    def __init__(self, tree):
        self.tree = tree

    def compile(self) -> BytesIO:
        bio = BytesIO()

        for element in self.tree:
            element.compile(bio)

        return bio
