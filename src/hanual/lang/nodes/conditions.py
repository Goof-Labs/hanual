from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Union

from hanual.compile.constants.constant import Constant
from hanual.compile.instruction import *
from hanual.compile.registers import Registers
from hanual.exec.result import Result
from hanual.exec.wrappers import LiteralWrapper, hl_wrap
from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.exec.scope import Scope


class Condition(BaseNode, ABC):
    __slots__ = "_op", "_left", "_right", "_lines", "_line_no"

    def __init__(self: BaseNode, op: Token, left, right, lines: str, line_no: int) -> None:
        self._right: Union[Token, BaseNode] = right
        self._left: Union[Token, BaseNode] = left
        self._op: Token = op

        self._line_no = line_no
        self._lines = lines

    @property
    def op(self):
        return self._op

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def compile(self):
        instructions = []
        # LEFT SIDE

        reg_l = new_reg()
        reg_r = new_reg()

        if isinstance(self._left, Token):
            if self._left.type in ("STR", "INT"):
                instructions.append(MOV_RC[reg_l, Constant(self._left.value)])

            elif self._left.type == "ID":
                instructions.append(CPY[reg_l, Constant(self._left.value)])

        else:
            instructions.extend(self._left.compile())
            instructions.append(MOV_RR[reg_l, Registers.R])

        # RIGHT SIDE
        if isinstance(self._right, Token):
            if self._right.type in ("STR", "INT"):
                instructions.append(MOV_RC[reg_r, Constant(self._right.value)])

            elif self._right.type == "ID":
                instructions.append(CPY[reg_r, Constant(self._right.value)])

        else:
            instructions.extend(self._right.compile())
            instructions.append(MOV_RR[reg_r, Registers.R])

        instructions.append(EXC[self._op.value, reg_l, reg_r])
        instructions.append(CMP[None])

        return instructions

    def get_constants(self) -> list[Constant]:
        if isinstance(self._left, Token):
            if self._left.type in ("STR", "NUM"):
                yield Constant(self._left.value)

        else:
            yield from self._left.get_constants()

        if isinstance(self._right, Token):
            if self._right.type in ("STR", "NUM"):
                yield Constant(self._right.value)

        else:
            yield from self._left.get_constants()

    def get_names(self) -> list[str]:
        names = []

        if isinstance(self._left, Token):
            if self._left.type == "ID":
                names.append(self._left.value)

        else:
            names.extend(self._left.get_names())

        if isinstance(self._right, Token):
            if self._right.type == "ID":
                names.append(self._right.value)

        else:
            names.extend(self._right.get_names())

        return names

    def execute(self, scope: Scope) -> Result[Any, LiteralWrapper[bool]]:
        res = Result()

        # get left and right
        left, error = res.inherit_from(self._get_value(scope, self._left))

        if error:
            return res

        left = left.value

        right, error = res.inherit_from(self._get_value(scope, self._right))

        if error:
            return res

        right = right.value

        if self._op.value == "==":
            return res.success(left == right)

        elif self._op.value == "!=":
            return res.success(left != right)

        elif self._op.value == ">":
            return res.success(left > right)

        elif self._op.value == "<":
            return res.success(left < right)

        elif self._op.value == ">=":
            return res.success(left >= right)

        elif self._op.value == "<=":
            return res.success(left <= right)

        elif self._op.value == "===":
            return res.success((left == right) and (isinstance(left, type(right))))

        else:
            raise NotImplementedError(f"{self._op!r} not accounted for")

    @staticmethod
    def _get_value(scope: Scope, value: Any) -> Result:
        if isinstance(value, Token):
            return hl_wrap(scope, value)

        else:
            return value.execute(scope)
