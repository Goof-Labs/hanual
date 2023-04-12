from __future__ import annotations

from abc import ABC

from typing import TypeVar, Any, Generic
from hanual.lang.context import Context
from hanual.lang.lexer import Token
from .base_node import BaseNode


O = TypeVar("O", Token, ...)  # Operator
L = TypeVar("L", Token, Any)  # Left
R = TypeVar("R", Token, Any)  # Right


class BinOpNode(BaseNode, ABC, Generic[O, L, R]):
    __slots__ = "_right", "_left", "_op"

    def __init__(self, op: O, left: L, right: R) -> None:
        self._right: R = right
        self._left: L = left

        self._op: O = op

    @property
    def left(self) -> L:
        """The left property."""
        return self._left

    @property
    def right(self) -> R:
        """The right property."""
        return self._right

    @property
    def op(self) -> O:
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

    def compile(self) -> Any:
        return super().compile()

    def __str__(self, level=0) -> str:
        return f"{type(self).__name__}(\n{' '.rjust(level)}op = {self.op.__str__(level+1) if issubclass(type(self.op), BaseNode) else str(str(self.op))}\n{' '.rjust(level)} left = {self.left.__str__(level+1) if issubclass(type(self.left), BaseNode) else str(str(self.left))}\n{' '.rjust(level)} right = {self.right.__str__(level+1) if issubclass(type(self.right), BaseNode) else str(str(self.right))})\n"
