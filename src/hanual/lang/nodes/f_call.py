from __future__ import annotations


from hanual.compile.registers import Registers
from hanual.compile.constant import Constant
from hanual.compile.instruction import *
from typing import TYPE_CHECKING, Union
from hanual.compile.label import Label
from hanual.compile.refs import Ref
from hanual.lang.lexer import Token
from .dot_chain import DotChain
from .base_node import BaseNode

if TYPE_CHECKING:
    from .arguments import Arguments


class FunctionCall(BaseNode):
    def __init__(self: BaseNode, name: Token, arguments: Arguments) -> None:
        self._name: Union[Token, DotChain] = name
        self._args: Arguments = arguments

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def compile(self):
        instructions = []

        ret_lbl = Label("RETURL-LBL", mangle=True)

        instructions.extend(self._args.compile())

        instructions.append(MOV_RI[Registers.O.value, ret_lbl.index])
        instructions.append(MOV_RF[Registers.F.value, Ref[self._name.value]])
        instructions.append(CALL[None])

        instructions.append(ret_lbl)

        return instructions

    def execute(self):
        raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        return self._args.get_constants()

    def get_names(self):
        yield self._name.value
        yield from self._args.get_names()

    def find_priority(self) -> list[BaseNode]:
        return []
