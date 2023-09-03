from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar, Union, Optional, Generator
from hanual.compile.constants.constant import Constant
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.builtin_lexer import Token
from hanual.compile.instruction import *
from hanual.exec.wrappers import hl_wrap
from hanual.exec.result import Result

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager
    from .f_def import FunctionDefinition
    from hanual.exec.scope import Scope

T = TypeVar("T")


class Arguments(BaseNode):
    def __init__(self, children: Union[T, List[T]]) -> None:
        self._children: List[T] = []
        self.function_def = False

        if isinstance(children, Token):
            # if children.type == "ID":
            #     self._children: List[T] = [children.value]

            # else:
            #     self._children: List[T] = [children]
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

    def _gen_args(self, names, scope: Scope) -> Generator[Result, None, None]:
        res = Result()

        for name, value in zip(names, self._children):
            # token
            if isinstance(value, Token):
                val, err = res.inherit_from(hl_wrap(scope=scope, value=value.value))

                if err:
                    yield res.fail(err)

                yield res.success((name, val))

            # can be executed
            else:
                # value = the bin op node, val = what was returned
                val, err = res.inherit_from(value.execute(scope=scope))

                if err:
                    yield res.fail(err)

                val, err = res.inherit_from(hl_wrap(scope=scope, value=val))

                yield res.success((name, val))

    def execute(self, scope, initiator: Optional[str] = None):
        res = Result()

        if initiator is None:
            raise Exception(f"can't run without initiator")

        func: Union[FunctionDefinition, None] = scope.get(initiator, None)

        if func is None:
            raise Exception(f"can't find func {initiator!r}")

        args = {}

        for resp in self._gen_args(names=func.arguments.children, scope=scope):
            if resp.error:
                return res.fail(resp.error)

            val, err = res.inherit_from(resp)

            if err:
                return res

            args[resp.response[0] if isinstance(resp.response[0], str) else resp.response[0].value] = val[1]

        return res.success(args)

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
