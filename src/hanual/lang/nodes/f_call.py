from __future__ import annotations

from hanual.compile.constants.constant import Constant
from typing import TYPE_CHECKING, Union, Callable
from hanual.compile.registers import Registers
from hanual.compile.instruction import *
from hanual.compile.label import Label
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from hanual.compile.refs import Ref
from hanual.lang.lexer import Token
from .base_node import BaseNode
from .dot_chain import DotChain

if TYPE_CHECKING:
    from hanual.compile.compile_manager import CompileManager
    from .arguments import Arguments


class FunctionCall(BaseNode):
    __slots__ = "_name", "_args",

    def __init__(self: BaseNode, name: Token, arguments: Arguments) -> None:
        self._name: Union[Token, DotChain] = name
        self._args: Arguments = arguments

    @property
    def name(self) -> Token:
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

        f_scope = Scope(parent=scope, name=self._name.value)

        # get the arguments from the parent scope and give them a new alias, then check for errors and return if so

        arg_res = self._args.execute(scope=scope, initiator=self._name.value)
        args, err = arg_res
        res.inherit_from(arg_res)

        if res.error:
            return res

        f_scope.extend(args)

        # run the body

        func: Union[Callable] = scope.get(self._name.value, None)
        if not func:
            return res.fail(f"{self._name.value!r} was not found")

        res.inherit_from(func(scope=f_scope))

        return res

    def get_constants(self) -> list[Constant]:
        return self._args.get_constants()

    def get_names(self):
        yield self._name.value
        yield from self._args.get_names()

    def find_priority(self) -> list[BaseNode]:
        return []
