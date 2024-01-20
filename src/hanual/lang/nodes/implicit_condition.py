from __future__ import annotations

from typing import TYPE_CHECKING

from bytecode import Compare, Instr

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.f_call import FunctionCall
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.util import Response, Request

if TYPE_CHECKING:
    ...


class ImplicitCondition[OP: Token, V: (Token, FunctionCall)](BaseNode):
    __slots__ = (
        "_right",
        "_op",
        "_lines",
        "_line_range",
    )

    def __init__(self, op: OP, val: V) -> None:
        self._right: V = val
        self._op: OP = op

    @property
    def value(self) -> V:
        return self._right

    @property
    def op(self) -> OP:
        return self._op

    def gen_code(self) -> GENCODE_RET:
            inferred: object | None = ctx.get("infer")

            if inferred is None or not isinstance(inferred, Token):
                raise TypeError(f"infer was left blank for {type(self).__name__}.gen_code")

            # implement context here
            yield from inferred.gen_code()
            yield from self._right.gen_code()

            if self._op.value == "==":
                yield Response(Instr("COMPARE_OP", Compare.EQ))

            elif self._op.value == ">":
                yield Response(Instr("COMPARE_OP", Compare.GT))

            elif self._op.value == "<":
                yield Response(Instr("COMPARE_OP", Compare.LT))

            elif self._op.value == ">=":
                yield Response(Instr("COMPARE_OP", Compare.GE))

            elif self._op.value == "<=":
                yield Response(Instr("COMPARE_OP", Compare.LE))

            elif self._op.value == "!=":
                yield Response(Instr("COMPARE_OP", Compare.NE))

            else:
                raise NotImplementedError(f"Have not implemented operator {self._op.value}")

    def prepare(self) -> PREPARE_RET:
        yield from self._right.prepare()
