from __future__ import annotations

from typing import TYPE_CHECKING

from bytecode import BinaryOp, Instr

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.util import Response
from hanual.lang.util.node_utils import Intent

if TYPE_CHECKING:
    from hanual.lang.util.compileable_object import CompilableObject


class BinOpNode(BaseNode):
    __slots__ = "_right", "_left", "_op", "_lines", "_line_range"

    def __init__(
            self,
            op: Token,
            left: CompilableObject,
            right: CompilableObject,
    ) -> None:
        self._right: CompilableObject = right
        self._left: CompilableObject = left

        self._op: Token = op

    @property
    def left(self) -> CompilableObject:
        return self._left

    @property
    def right(self) -> CompilableObject:
        return self._right

    @property
    def op(self) -> Token:
        return self._op

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
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

    def prepare(self) -> PREPARE_RET:
        yield from self._left.prepare()
        yield from self._right.prepare()
