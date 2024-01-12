from __future__ import annotations

from typing import TYPE_CHECKING

from bytecode import BinaryOp, Instr

from hanual.compile.context import Context
from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.util import Response, Request, Reply

if TYPE_CHECKING:
    from hanual.lang.nodes.f_call import FunctionCall


class ImplicitBinOp[O: Token, R: (Token, FunctionCall)](BaseNode):
    __slots__ = ("_right", "_op", "_lines", "_line_range")

    def __init__(self, op: O, right: R) -> None:
        # The left side is implied
        self._right = right
        self._op = op

    @property
    def op(self) -> O:
        return self._op

    @property
    def right(self) -> R:
        return self._right

    def gen_code(self) -> GENCODE_RET:
        reply: Reply[Context] | None = yield Request(Request.GET_CONTEXT)
        assert reply is not None

        with reply.response as ctx:
            ctx.add(store=True)

            inferred: Token | object | None = ctx.get('infer')

            if inferred is None or not isinstance(inferred, Token):
                raise TypeError(
                    f"Argument 'infer' was left blank in '{type(self).__name__}.gen_code'"
                )

            yield from inferred.gen_code()
            yield from self._right.gen_code()

            if self._op.value == "+":
                yield Response(Instr("BINARY_OP", BinaryOp.ADD))

            else:
                raise NotImplementedError(f"Have not implemented operator {self._op.value}")

            yield from inferred.gen_code()

    def prepare(self) -> PREPARE_RET:
        yield from self._right.prepare()
