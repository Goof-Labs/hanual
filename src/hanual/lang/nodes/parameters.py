from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar, Union, Optional
from hanual.compile.constants.constant import Constant
from hanual.lang.nodes.arguments import Arguments
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.builtin_lexer import Token
from hanual.compile.instruction import *
from hanual.exec.result import Result
from .f_def import FunctionDefinition

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager

T = TypeVar("T")


class Parameters(BaseNode):
    def __init__(self, children: Union[T, List[T]]) -> None:
        self._children: List[T] = []

        if isinstance(children, Token):
            self._children: List[T] = [children.value]

        elif isinstance(children, (Parameters, Arguments)):
            self._children = children.children

        elif issubclass(type(children), BaseNode):
            self._children: List[T] = [children]

        else:  # This is just another node that we have chucked into a list
            self._children: List[T] = list(children)

    def add_child(self, child):
        if isinstance(child, Parameters):
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
        args = {k: v.value for k, v in zip(func.arguments.children, self._children)}
        return Result().success(args)

    def get_names(self) -> list[Token]:
        names: List[Token] = []

        for child in self._children:
            if isinstance(child, Token):
                if child.type == "ID":
                    names.append(child)

        return names

    def get_constants(self) -> list[Constant]:
        return []

    def find_priority(self) -> list[BaseNode]:
        return []
