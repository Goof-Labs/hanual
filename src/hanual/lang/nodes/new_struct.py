from __future__ import annotations


from typing import TYPE_CHECKING, Any, Dict
from hanual.lang.lexer import Token
from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.compile.ir import IR
    from .arguments import Arguments
    from .f_call import FunctionCall


class NewStruct(BaseNode):
    def __init__(self: BaseNode, call: FunctionCall) -> None:
        self._args: Arguments = call.args
        self._name: Token = call.name

    @property
    def name(self) -> FunctionCall:
        return self._name

    @property
    def args(self) -> FunctionCall:
        return self._args

    def compile(self, ir: IR, to: str) -> None:
        for arg in self._args.children:
            if isinstance(arg, Token):
                if arg.type == "NUM":
                    ir.mov("FA", ir.int_con(arg.value))

                elif arg.type == "STR":
                    ir.mov("FA", ir.str_con(arg.value))

                else:
                    raise Exception()

            elif hasattr(arg, "compile"):
                reg = ir.reserve_reg()

                arg.compile(ir, to=reg)
                ir.mov("FA", reg, append=True)

                ir.free_reg(reg)

            else:
                raise Exception

        ir.mov("FP", self._name)

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
