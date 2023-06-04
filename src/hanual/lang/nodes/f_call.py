from __future__ import annotations


from typing import Any, Dict, TYPE_CHECKING, Union

from hanual.compile.state_fragment import Fragment, MOV, MKPTR, CAL, Registers
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
from hanual.lang.errors import Error
from hanual.lang.lexer import Token
from .dot_chain import DotChain
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.runtime import RuntimeEnvironment, ExecStatus
    from hanual.lang.errors import Error
    from .arguments import Arguments


class FunctionCall(BaseNode):
    def __init__(self: BaseNode, name: Token, arguments: Arguments) -> None:
        self._name: Union[Token, DotChain] = name
        self._args: Arguments = arguments

    def compile(self) -> None:
        frg = Fragment()

        for arg in self._args.children:
            if isinstance(arg, Token):
                if arg.type == "ID":
                    frg.add_instr(MOV(MKPTR(arg.value), Registers.FA))

                elif arg.type == "STR":
                    frg.add_instr(MOV(frg.add_const(arg.value), Registers.FA))

                else:
                    raise NotImplementedError(arg)

            else:
                arg.compile(to=Registers.FA)

        id_ = frg.add_external_func(self._name.value)
        frg.add_instr(MOV(to=Registers.FP, frm=id_))
        frg.add_instr(CAL())

        return frg

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def as_dict(self) -> Dict[str, Any]:
        return {"args": self._args.as_dict(), "name": self._name}
