from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from bytecode import Instr, BinaryOp

from hanual.compile.context import Context
from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Response, Request

if TYPE_CHECKING:
    pass


class BinOpNode[L: (Token, BaseNode), R: (Token, BaseNode)](BaseNode):
    __slots__ = "_right", "_left", "_op", "_lines", "_line_range"

    def __init__(
        self,
        op: Token,
        left: L,
        right: R,
    ) -> None:
        self._right: R = right
        self._left: L = left

        self._op: Token = op

    @property
    def left(self) -> L:
        return self._left

    @property
    def right(self) -> R:
        return self._right

    @property
    def op(self) -> Token:
        return self._op

    def gen_code(self, **kwargs) -> Generator[Response | Request, Reply, None]:
        context: Context = (yield Request[Context](Request.CREATE_CONTEXT)).response

        with context:
            context.add(parent=self)

            yield from self._left.gen_code()
            yield from self._right.gen_code()

            if self._op.value == "+":
                yield Response(
                    Instr("BINARY_OP", BinaryOp.ADD, location=self.get_location())
                )

            elif self._op.value == "-":
                yield Response(
                    Instr("BINARY_OP", BinaryOp.SUBTRACT, location=self.get_location())
                )

            elif self._op.value == "/":
                yield Response(
                    Instr(
                        "BINARY_OP", BinaryOp.TRUE_DIVIDE, location=self.get_location()
                    )
                )

            elif self._op.value == "*":
                yield Response(
                    Instr("BINARY_OP", BinaryOp.MULTIPLY, location=self.get_location())
                )

            else:
                raise NotImplementedError(
                    f"operator {self._op.value!r} has not been implemented yet"
                )

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        yield from self._left.prepare()
        yield from self._right.prepare()
