from __future__ import annotations

from hanual.compile import GlobalState, Instruction, InstructionEnum
from typing import TypeVar, Union, List, Any
from hanual.lang.builtin_lexer import Token
from .base_node import BaseNode
from io import StringIO

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
        res = []

        for node in self._children:
            if isinstance(node, Token):
                # We add a constant and get the index back
                idx = global_state.constants.add_const(node.value)
                res.append(Instruction(InstructionEnum.PGC, idx))

            else:
                res.append(node.compile(global_state))

        return res

    def __str__(self, level=1) -> str:
        string = StringIO()

        string.write(f"{type(self).__name__}([\n".rjust(level))

        for child in self._children:
            string.write(str(child) + "\n")

        string.write("])".rjust(level))

        return string.getvalue()
