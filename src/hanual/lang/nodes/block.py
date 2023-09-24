from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, List, Optional, TypeVar, Union

from hanual.exec.result import Result
from hanual.exec.scope import Scope

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager
    from hanual.compile.constants.constant import BaseConstant

T = TypeVar("T")


class CodeBlock(BaseNode, ABC):
    __slots__ = ("_children", "_line_no", "_lines")

    def __init__(self, children: Union[List[T], T], lines: str, line_no: int) -> None:
        self._children: List[BaseNode] = []
        self.add_child(children)

        self._line_no = line_no
        self._lines = lines

    def add_child(self, child: CodeBlock):
        if isinstance(child, (list, tuple)):
            for child_ in child:
                self.add_child(child_)

        elif isinstance(child, CodeBlock):
            self.children.extend(child.children)

        else:
            self._children.append(child)

        return self

    def execute(self, scope: Scope) -> Result:
        res = Result()

        for child in self._children:
            # If we have an error then we raise it, otherwise I just discard the return value and keep going
            res.inherit_from(child.execute(scope=scope))

            if res.error:
                return res

        return res

    def compile(self, cm: CompileManager) -> Any:
        instructions = []

        for child in self.children:
            instructions.extend(child.compile(cm=cm))

        return instructions

    def get_constants(self) -> list[BaseConstant]:
        for node in self._children:
            yield from node.get_constants()

    def get_names(self) -> list[str]:
        lst = []

        for node in self._children:
            lst.extend(node.get_names())

        return lst

    @property
    def children(self):
        return self._children
