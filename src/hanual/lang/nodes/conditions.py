from __future__ import annotations

from bytecode import Instr, Compare
from typing import TYPE_CHECKING, Generator

from hanual.util import Reply, Response, Request
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.lexer import Token

if TYPE_CHECKING:
    pass


class Condition[L: (Token, BaseNode), R: (Token, BaseNode)](BaseNode):
    __slots__ = "_op", "_left", "_right", "_lines", "_line_range"

    def __init__(self, op: Token, left, right) -> None:
        self._right: R = right
        self._left: L = left
        self._op: Token = op

    @property
    def op(self) -> Token:
        return self._op

    @property
    def left(self) -> L:
        return self._left

    @property
    def right(self) -> R:
        return self._right

    def gen_code(self, **kwargs) -> Generator[Response | Request, Reply, None]:
        # TODO : addd context
        yield from self._left.gen_code()
        yield from self._right.gen_code()

        if self._op.value == "==":
            yield Response(
                Instr("COMPARE_OP", Compare.EQ, location=self.get_location())
            )

        elif self._op.value == ">":
            yield Response(
                Instr("COMPARE_OP", Compare.GT, location=self.get_location())
            )

        elif self._op.value == "<":
            yield Response(
                Instr("COMPARE_OP", Compare.LT, location=self.get_location())
            )

        elif self._op.value == ">=":
            yield Response(
                Instr("COMPARE_OP", Compare.GE, location=self.get_location())
            )

        elif self._op.value == "<=":
            yield Response(
                Instr("COMPARE_OP", Compare.LE, location=self.get_location())
            )

        elif self._op.value == "!=":
            yield Response(
                Instr("COMPARE_OP", Compare.NE, location=self.get_location())
            )

        else:
            raise NotImplementedError(f"Have not implemented operator {self._op.value}")

    def prepare(self) -> Generator[Request, Reply, None]:
        yield from self._left.prepare()
        yield from self._right.prepare()
