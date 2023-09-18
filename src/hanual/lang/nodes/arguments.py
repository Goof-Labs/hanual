from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar, Union, Optional, Generator
from hanual.compile.constants.constant import Constant
from hanual.exec.wrappers.literal import LiteralWrapper
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.builtin_lexer import Token
from hanual.compile.instruction import *
from hanual.exec.wrappers import hl_wrap
from hanual.exec.result import Result
from hanual.lang.errors import Frame

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager
    from hanual.lang.nodes import Parameters
    from .f_def import FunctionDefinition
    from hanual.exec.scope import Scope

T = TypeVar("T", bound=BaseNode)


class Arguments(BaseNode):
    __slots__ = "function_def", "_children",

    def __init__(self, children: Union[T, List[T]]) -> None:
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
            self._children: List[T] = list(*children)

    def add_child(self, child):
        if isinstance(child, Arguments):
            self._children.extend(child.children)

        else:
            self._children.append(child)

        return self

    @property
    def children(self) -> List:
        return self._children

    def compile(self, cm: CompileManager):
        return [UPK(self._children)]

    def _gen_args(self, names, scope: Scope) -> Generator[Result, None, None]:
        res = Result()

        for name, value in zip(names, self._children):
            # token
            if isinstance(value, Token):
                if value.type in ("STR", "NUM"):
                    assert isinstance(value.value, LiteralWrapper), f"Expected a LiteralWrapper got {type(value.value).__name__!r} instead"
                    # the value should already be a `LiteralWrapper`
                    yield res.success(value)

                else: # The token is an ID
                    _, err = res.inherit_from(scope.get(str(value.value), None))

                    if err:
                        return err.add_frame(Frame("arguments")) 

                    yield res

                val, err = res.inherit_from(hl_wrap(scope=scope, value=value))

                if err:
                    yield res.fail(err.add_frame(Frame("arguments")))

                yield res.success((name, val))
                continue

            # can be executed
            # value = the bin op node, val = what was returned
            val, err = res.inherit_from(value.execute(scope=scope))

            if err:
                yield res.fail(err.add_frame(Frame(name="arguments")))
                return

            val, err = res.inherit_from(hl_wrap(scope=scope, value=val))

            yield res.success((name, val))

    def execute(self, scope, initiator: Optional[str] = None, params: Optional[Parameters] = None):
        res = Result()

        if initiator is None and params is None:
            raise Exception(f"can't run without initiator or params")

        # if `initiator` param was supplied
        if initiator:
            func: Union[FunctionDefinition, None] = scope.get(initiator, None)

            if func is None:
                raise Exception(f"can't find func {initiator!r}")

            func_params = func.arguments.children

        # `params`
        if params:
            func_params = params.children

        args = {}

        for resp in self._gen_args(names=func_params, scope=scope):
            if resp.error:
                return res.fail(resp.error.add_frame(Frame("arguments")))

            val, err = res.inherit_from(resp)

            if err:
                return res

            # set the arg equal to the value
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
