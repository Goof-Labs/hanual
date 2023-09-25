from __future__ import annotations

from typing import TYPE_CHECKING, Generator, List, Optional, TypeVar, Union

from hanual.compile.constants.constant import Constant
from hanual.compile.instruction import *
from hanual.exec.result import Result
from hanual.exec.wrappers.literal import LiteralWrapper
from hanual.lang.builtin_lexer import Token
from hanual.lang.errors import Frame
from hanual.lang.nodes.base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager
    from hanual.exec.scope import Scope
    from hanual.lang.nodes import Parameters

    from .f_def import FunctionDefinition

T = TypeVar("T")


class Arguments(BaseNode):
    __slots__ = (
        "_children",
        "_lines",
        "_line_no",
    )

    def __init__(self, children: Union[T, List[T]], lines: str, line_no: int) -> None:
        if isinstance(children, Token):
            self._children: List[T] = [children]

        elif issubclass(type(children), BaseNode):
            self._children: List[T] = [children]

        else:  # This is just another node that we have chucked into a list
            self._children: List[T] = list(*children)

        self._line_no = line_no
        self._lines = lines

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
                    assert isinstance(
                        value.value, LiteralWrapper
                    ), f"Expected a LiteralWrapper got {type(value.value).__name__!r} instead"
                    # the value should already be a `LiteralWrapper`
                    yield res.success(value)

                else:  # The token is an ID
                    val, err = res.inherit_from(scope.get(str(value.value), res=True))

                    if err:
                        return err.add_frame(Frame(name=type(self).__name__, line=self.lines, line_num=self.line_no))

                    yield res.success((name, val))

                # val, err = res.inherit_from(hl_wrap(scope=scope, value=value))

                # if err:
                #    yield res.fail(err.add_frame(Frame("arguments")))

                if isinstance(value, LiteralWrapper):
                    yield res.success((name, value))

                elif isinstance(value, Token) and isinstance(
                    value.value, LiteralWrapper
                ):
                    yield res.success((name, value.value))

                elif isinstance(value, Token) and value.type == "ID":
                    val, err = scope.get(str(value.value), res=True)

                    if err:
                        return err.add_frame(Frame(name=type(self).__name__, line=self.lines, line_num=self.line_no))

                    yield res.success((name, val))

                else:
                    raise Exception(value)
                continue

            # can be executed
            # value = the bin op node, val = what was returned
            val, err = res.inherit_from(value.execute(scope=scope))

            if err:
                yield res.fail(err.add_frame(Frame(name=type(self).__name__, line=self.lines, line_num=self.line_no)))
                return

            # val, err = res.inherit_from(hl_wrap(scope=scope, value=val))

            if not (
                isinstance(val, LiteralWrapper) or isinstance(val.value, LiteralWrapper)
            ):
                raise Exception(val)

            # if the val is a `Token` then get it's value
            if isinstance(val, Token):
                val = val.value

            yield res.success((name, val))

    def execute(
        self,
        scope,
        initiator: Optional[str] = None,
        params: Optional[Parameters] = None,
    ):
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
        else:
            func_params = params.children

        args = {}

        for resp in self._gen_args(names=func_params, scope=scope):
            if resp.error:
                return res.fail(resp.error.add_frame(Frame(name=type(self).__name__, line=self.lines, line_num=self.line_no)))

            val, err = res.inherit_from(resp)

            if err:
                return res

            # set the arg equal to the value
            args[
                resp.response[0]
                if isinstance(resp.response[0], str)
                else resp.response[0].value
            ] = resp.response[1]
        return res.success(args)

    def get_names(self) -> list[Token]:
        names: List[Token] = []

        for child in self._children:
            if isinstance(child, Token):
                if child.type == "ID":
                    names.append(child)

        return names

    def get_constants(self) -> list[Constant]:
        # function definitions can't have constants as arguments
        # like does this make any sense
        # def spam(1, 2, 3, 4): ...
        lst = []

        for child in self._children:
            if isinstance(child, Token):
                if child.type in ("STR", "NUM"):
                    lst.append(Constant(child.value))

            else:
                lst.extend(child.get_constants())

        return lst
