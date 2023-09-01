from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar, Union, Optional
from hanual.compile.constants.constant import Constant
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.builtin_lexer import Token
from hanual.compile.instruction import *
from hanual.exec.result import Result
from .f_def import FunctionDefinition

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager

T = TypeVar("T")


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

    def compile(self, cm: CompileManager):
        return [UPK(self._children)]

    def execute(self, scope, initiator: Optional[str] = None):
        # TODO: errors
        func: Union[FunctionDefinition, None] = scope.get(initiator, None)
        print("I:", initiator)
        print("S:", scope._env)
        args = {k: v.value for k, v in zip(func.arguments.children, self._children)}
        return Result().success(args)

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
