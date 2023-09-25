from __future__ import annotations

from typing import TYPE_CHECKING, Union

from hanual.compile.constants.constant import Constant
from hanual.compile.instruction import *
from hanual.compile.label import Label
from hanual.compile.refs import Ref
from hanual.compile.registers import Registers
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack
from hanual.lang.lexer import Token

from .base_node import BaseNode
from .dot_chain import DotChain

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager

    from .arguments import Arguments


class FunctionCall(BaseNode):
    __slots__ = (
        "_name",
        "_args",
        "_lines",
        "_line_no",
    )

    def __init__(self, name: Token, arguments: Arguments, lines: str, line_no: int) -> None:
        self._name: Union[Token, DotChain] = name
        self._args: Arguments = arguments

        self._line_no = line_no
        self._lines = lines

    @property
    def name(self) -> Union[Token, DotChain]:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def compile(self, cm: CompileManager):
        instructions = []

        ret_lbl = Label("RETURN-LBL", mangle=True)

        instructions.extend(self._args.compile(cm=cm))

        instructions.append(MOV_RI[Registers.O.value, ret_lbl.index])
        instructions.append(MOV_RF[Registers.F.value, Ref[self._name.value, cm]])
        instructions.append(CALL[None])

        instructions.append(ret_lbl)

        return instructions

    def execute(self, scope: Scope) -> Result:
        res = Result()

        # create a scope for the function
        if isinstance(self._name, Token):
            f_scope = Scope(
                parent=scope,
                frame=Frame(
                    name=str(self.name),
                    line_range=self.line_no,
                    line=self.lines,
                ),
            )
            func = scope.get(str(self._name.value), None)

            # check for errors
            if func is None:
                return res.fail(
                    HanualError(
                        pos=(
                            self._name.line,
                            self._name.colm,
                            self._name.colm + len(self._name.value),
                        ),
                        line=self._name.line_val,
                        name=ErrorType.unresolved_name,
                        reason=f"Couldn't resolve reference to {self._name.value!r}",
                        tb=TraceBack().add_frame(Frame(name=type(self).__name__, line=self.lines, line_num=self.line_no)),
                        tip="Did you make a typo?",
                    )
                )

        elif isinstance(self._name, DotChain):
            # get the last name in the chain because that is what the function name is
            f_scope = Scope(
                parent=scope,
                frame=Frame(name=str(self._name.chain[0].value), line=self._lines, line_num=self.line_no))
            func, err = res.inherit_from(self._name.execute(scope))

            if func is None:
                return res.fail(err.add_frame(Frame(name=type(self).__name__, line=self.lines, line_num=self.line_no)))

        else:
            raise Exception

        # get the arguments from function just obtained
        arg_res = self._args.execute(scope=scope, params=func.arguments)
        args, err = arg_res
        res.inherit_from(arg_res)

        if res.error:
            return res

        f_scope.extend(args)

        # run the body
        _, err = res.inherit_from(func(scope=f_scope))

        return res

    def get_constants(self) -> list[Constant]:
        yield from self._args.get_constants()

    def get_names(self):
        yield self._name.value
        yield from self._args.get_names()
