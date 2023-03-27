from __future__ import annotations

from abc import ABC

from typing import TypeVar, Union, Any
from .base_node import BaseNode
from .context import Context
from lexer import Token


T = TypeVar("T", bound=BaseNode)


class BinOpNode(BaseNode, ABC):
    def __init__(
        self, op: Token, left: Union[Token, T], right: Union[Token, T]
    ) -> None:
        self._op: Token = op
        self._left: Union[Token, T] = left
        self._right: Union[Token, T] = right

    @property
    def left(self):
        """The left property."""
        return self._left

    @property
    def right(self):
        """The right property."""
        return self._right

    @property
    def op(self):
        """The op property."""
        return self._op

    def __format__(self, spec: str) -> str:
        """
        %l => left operator
        %r => right operator
        %o => operator
        """

        perc = False
        res = ""

        for char in spec:
            if perc:  # then check characters
                perc = False

                if char == "l":
                    res += self.left

                elif char == "r":
                    res += self.right

                elif char == "o":
                    res += self.op

                elif char == "%":
                    res += "%"

                else:
                    res += "%" + char

            if char == "%":
                perc = True

        return res

    def eval(self: BinOpNode, context: Context) -> int:
        # LEFT
        if isinstance(self._left, Token):
            left = self._left.value

        # elif context.is_variable(self._left.value):
        #     left = context.get_variable_value(self._left.value)

        else:
            left = self._left.eval(context)

        # RIGHT
        if isinstance(self._right, Token):
            right = self._right.value

        # elif context.is_variable(self._right.value):
        #     right = context.get_variable_value(self._right.value)

        else:
            right = self._right.eval(context)

        if self._op.value == "+":
            return left + right

        elif self._op.value == "-":
            return left - right

        elif self._op.value == "/":
            return left / right

        elif self._op.value == "*":
            return left * right

        elif self._op.value == "%":
            return left % right

        elif self._op.value == "//":
            return left // right

        elif self._op.value == "^":
            return left**right

        elif self._op.value == "<<":
            return left << right

        elif self._op.value == ">>":
            return left >> right

        else:
            raise Exception("'%s' is not an arithmatic operation", (self._op.value,))
