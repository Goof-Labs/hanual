from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Optional

from bytecode import Instr, Compare

from hanual.lang.lexer import Token
from .base_node import BaseNode
from .f_call import FunctionCall
from hanual.util import Reply, Response, Request, REQUEST_TYPE

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

    def gen_code(self) -> Generator[Response[Instr] | Request[REQUEST_TYPE], Optional[Reply], None]:
        # TODO implement context

        infered: Token = kwargs.get("infer", None)

        if infered is None:
            raise TypeError(f"infer was left blank for {type(self).__name__}.gen_code")

        # implement context here
        yield from infered.gen_code()
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

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        yield from self._right.prepare()
