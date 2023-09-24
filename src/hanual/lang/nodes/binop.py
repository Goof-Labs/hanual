from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Union

from hanual.compile.constants.constant import Constant
from hanual.compile.instruction import *
from hanual.compile.registers import Registers
from hanual.exec.result import Result
from hanual.exec.scope import Scope
from hanual.exec.wrappers import LiteralWrapper
from hanual.exec.wrappers.wrap import hl_wrap
from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack
from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    ...


class BinOpNode(BaseNode, ABC):
    __slots__ = "_right", "_left", "_op"

    def __init__(self, op: Token, left, right) -> None:
        self._right: Union[Token, BinOpNode] = right
        self._left: Union[Token, BinOpNode] = left

        self._op: Token = op

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def op(self):
        return self._op

    def compile(self):
        instructions = []

        reg_1 = new_reg()
        reg_2 = new_reg()

        # LEFT SIDE
        if isinstance(self._left, Token):
            if self._left.type in ("STR", "NUM"):
                instructions.append(MOV_RC[reg_1, Constant(self._left.value)])

            elif self._left.type == "ID":
                instructions.append(MOV_RC[reg_2, Constant(self._left.value)])

            else:
                raise NotImplementedError

        else:
            instructions.extend(self._left.compile())
            instructions.append(MOV_RR[reg_1, Registers.R])

        # RIGHT SIDE
        if isinstance(self._right, Token):
            if self._right.type in ("STR", "NUM"):
                instructions.append(MOV_RC[reg_2, Constant(self._right.value)])

            elif self._right.type == "ID":
                instructions.append(MOV_RC[reg_2, Constant(self._right.value)])

            else:
                raise NotImplementedError

        else:
            instructions.extend(self._right.compile())
            instructions.append(MOV_RR[reg_2, Registers.R])

        instructions.append(EXC[self._op.value, reg_1, reg_2])
        return instructions

    @staticmethod
    def _get_val(val: Any, scope: Scope) -> Result[LiteralWrapper, Any]:
        res = Result()

        if isinstance(val, Token):
            if val.type in ("STR", "NUM"):  # literal
                return res.success(val.value)

            elif val.type == "ID":
                return res.inherit_from(scope.get(str(val.value), res=True))

            else:
                raise Exception

        else:
            val, err = res.inherit_from(val.execute(scope=scope))

            if err:
                return res

            return res.success(LiteralWrapper(val))

    def execute(self, scope: Scope) -> Result[LiteralWrapper[float], str]:
        res = Result()

        # LEFT
        left, err = res.inherit_from(self._get_val(self._left, scope=scope))

        if err:
            return res

        left = left.value

        # make sure left is a literal
        if isinstance(left, LiteralWrapper):
            left = left.value

        # RIGHT
        right, err = res.inherit_from(self._get_val(self._right, scope=scope))

        if err:
            return res

        right = right.value

        # make sure right is a literal
        if isinstance(right, LiteralWrapper):
            right = right.value

        # OPERATIONS
        if self._op.value == "+":
            return res.success(LiteralWrapper(left + right))

        elif self._op.value == "-":
            return res.success(LiteralWrapper(left - right))

        elif self._op.value == "/":
            if right == 0:
                return res.fail(
                    HanualError(
                        pos=(self._op.line, self._op.colm, self._op.colm + 1),
                        line=self._op.line_val,
                        name=ErrorType.division_by_zero,
                        reason=f"Can't divide by zero",
                        tb=TraceBack().add_frame(Frame("binary operation")),
                        tip=f"Try validating {self._right.value!r}",
                    )
                )

            return res.success(LiteralWrapper(left / right))

        elif self._op.value == "*":
            return res.success(LiteralWrapper(left * right))

        else:
            raise NotImplementedError

    def get_constants(self) -> list[Constant]:
        consts = []

        if isinstance(self._left, Token):
            if self._left.type in ("STR", "NUM"):
                consts.append(Constant(self._left.value))

        else:
            consts.extend(self._left.get_constants())

        if isinstance(self._right, Token):
            if self._right.type in ("STR", "NUM"):
                consts.append(Constant(self._right.value))

        else:
            consts.extend(self._right.get_constants())

        return consts

    def get_names(self) -> list[str]:
        names = []

        if isinstance(self._left, Token):
            if self._left.type == "ID":
                names.append(self._left.value)

        if isinstance(self._right, Token):
            if self._right == "ID":
                names.append(self._right.value)

        return names
