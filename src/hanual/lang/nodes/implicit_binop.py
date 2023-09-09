from __future__ import annotations

from hanual.compile.compile_manager import CompileManager
from hanual.compile.constants.constant import Constant
from typing import TYPE_CHECKING, Union, Optional
from hanual.exec.wrappers import LiteralWrapper
from hanual.compile.registers import Registers
from hanual.compile.instruction import *
from hanual.exec.result import Result
from hanual.lang.lexer import Token
from .base_node import BaseNode
from hanual.lang.errors import ErrorType, HanualError, Frame, TraceBack


if TYPE_CHECKING:
    from hanual.exec.scope import Scope
    from .f_call import FunctionCall


class ImplicitBinOp(BaseNode):
    __slots__ = "_right", "_op",

    def __init__(self, op: Token, right: Union[Token, FunctionCall]) -> None:
        # The left side is implied
        self._right = right
        self._op = op

    @property
    def op(self) -> Token:
        return self._op

    @property
    def right(self) -> Union[Token, FunctionCall]:
        return self._right

    def compile(self, cm: CompileManager, name: str):
        instructions = []

        reg_1 = new_reg()
        reg_2 = new_reg()

        # LEFT SIDE
        instructions.append(MOV_RR[reg_2, name])

        # RIGHT SIDE
        if isinstance(self._right, Token):
            if self._right.type in ("STR", "NUM"):
                instructions.append(MOV_RC[reg_2, Constant(self._right.value)])

            elif self._right.type == "ID":
                instructions.append(MOV_RC[reg_2, Constant(self._right.value)])

            else:
                raise NotImplementedError

        else:
            instructions.extend(self._right.compile(cm))
            instructions.append(MOV_RR[reg_2, Registers.R])

        instructions.append(EXC[self._op.value, reg_1, reg_2])

        return instructions

    def execute(self, scope: Scope, name: Optional[str] = None) -> Result:
        res = Result()

        # get name
        if name is None:
            raise Exception(f"param 'name' was not passed")

        val = scope.get(name, None)

        if val is None:
            return res.fail(HanualError(
                    pos=(self._op.line, self._op.colm, self._op.colm+len(self._op.value)),
                    line=self._op.line_val,
                    name=ErrorType.unresolved_name,
                    reason=f"Couldn't resolve reference to {self._op.value!r}",
                    tb=TraceBack().add_frame(Frame("implicit binary op")),
                    tip="Did you make a typo?"
                ))

        if not isinstance(val, (float, int)):
            val = val.value

        # other

        if isinstance(self._right, Token):
            if self._right.type == "ID":
                other = scope.get(self._right.value, None)

            elif self._right.type == "STR":
                other = self._right.value

            elif self._right.type == "NUM":
                other = self._right.value

            else:
                raise Exception(f"{self._right!r} not accounted for")

        else:
            other, err = res.inherit_from(self._right.execute(scope=scope))

            if err:
                return res

            other = other.value

        if other is None:
            return res.fail(HanualError(
                    pos=(self._op.line, self._op.colm, self._op.colm+len(self._op.value)),
                    line=self._op.line_val,
                    name=ErrorType.unresolved_name,
                    reason=f"Couldn't resolve reference to {self._op.value!r}",
                    tb=TraceBack().add_frame(Frame("implicit binop")),
                    tip="Did you make a typo?"
                ))

        # math
        if self._op.value == "+":
            scope.set(name, LiteralWrapper(val+other))

            return Result().success(None)

        else:
            raise Exception(f"{self._op.value!r} not accounted for")

    def get_names(self) -> list[str]:
        if isinstance(self._right, Token):
            if self._right.type == "ID":
                return [self._right.value]

            else:
                return []

        else:
            return self._right.get_names()

    def get_constants(self) -> list[Constant]:
        if isinstance(self._right, Token):
            if self._right.type in ("STR", "NUM"):
                return [Constant(self._right.value)]

        else:
            return self._right.get_constants()

    def find_priority(self):
        return []
