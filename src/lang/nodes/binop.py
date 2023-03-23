from __future__ import annotations

from abc import ABC

from typing import TypeVar, Union, Any
from base_node import BaseNode
from context import Context
from ..lexer import Token


T = TypeVar("T", bound=BaseNode)


class BinOpNode(BaseNode, ABC):
    def __init__(self,
                 op: Token,
                 left: Union[Token, T],
                 right: Union[Token, T]) -> None:
        self._op: Token = op
        self._left: Union[Token, T] = left
        self._right: Union[Token, T] = right

    def eval(self: BinOpNode, context: Context) -> int:
        # LEFT
        if isinstance(self._left, Token):
            left = self._left.value

        # elif context.is_variable(self._left.value):
        #     left = context.get_variable_value(self._left.value)

        else:
            left = self._left.eval()

        # RIGHT
        if isinstance(self._right, Token):
            right = self._right.value

        # elif context.is_variable(self._right.value):
        #     right = context.get_variable_value(self._right.value)

        else:
            right = self._right.value

        if self._op.value == '+':
            return left + right

        elif self._op.value == '-':
            return left - right

        elif self._op.value == '/':
            return left / right

        elif self._op.value == '*':
            return left * right

        elif self._op.value == '%':
            return left % right

        elif self._op.value == '//':
            return left // right

        elif self._op.value == '^':
            return left ** right

        elif self._op.value == '<<':
            return left << right

        elif self._op.value == '>>':
            return left >> right

        else:
            raise Exception("'%s' is not an arithmatic operation", (self._op.value,))

    def compile(self) -> Any:
        # TODO: add compile method to 'BinOP'
        """
        This method has not been implemented yet,
        this would return the raw bytecode to
        evaluate the expression, or the result
        of the expression if it can be.
        >>> 1+(2*3)
        could be evaluated as 7, but if we had
        >>> 1+(foo * 3)
        this expression would not be evaluated,
        because it contains a variable.
        """
