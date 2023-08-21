from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar, Union

from hanual.compile.constant import Constant
from hanual.compile.instruction import *
from hanual.lang.builtin_lexer import Token
from hanual.lang.nodes.base_node import BaseNode

if TYPE_CHECKING:
    ...

T = TypeVar("T", Token, BaseNode)


class Arguments(BaseNode):
    def __init__(self, children: Union[T, List[T]]) -> None:
        self._children: List[T] = []
        self.function_def = False

        if isinstance(children, Token):
            self._children: List[T] = [children]

        elif issubclass(type(children), BaseNode):
            self._children: List[T] = [children]

        else:  # This is just another node that we have chucked into a list
            self._children: List[T] = list(children)

    def add_child(self, child):
        if isinstance(child, Arguments):
            self._children.extend(child.children)

        else:
            self._children.append(child)

        return self

    @property
    def children(self) -> List[T]:
        return self._children

    def compile(self):
        return [UPK(self._children)]

    def execute(self):
        raise NotImplementedError

    def get_names(self) -> list[Token]:
        names: List[Token] = []

        for child in self._children:
            if isinstance(child, Token):
                if child.type == "ID":
                    names.append(child)

            elif not self.function_def:
                names.extend(child.get_names())

        return names

    def get_constants(self) -> list[Constant]:
        # function definitions can't have constants as arguments
        # like does this make any sense
        # def spam(1, 2, 3, 4): ...
        if self.function_def:
            return []

        lst = []

        for child in self._children:
            if isinstance(child, Token):
                if child.type in ("STR", "NUM"):
                    lst.append(Constant(child.value))

            else:
                lst.extend(child.get_constants())

        return lst

    def find_priority(self) -> list[BaseNode]:
        return []
