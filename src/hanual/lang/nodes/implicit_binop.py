from __future__ import annotations

from typing import TYPE_CHECKING

from bytecode import BinaryOp, Instr

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent
from hanual.util import Response

if TYPE_CHECKING:
    from hanual.lang.nodes.f_call import FunctionCall
    from hanual.util.equal_list import ItemEqualList


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

    def gen_code(self, intents: ItemEqualList[Intent], **options) -> GENCODE_RET:
        inferred: Token = options.get("imply_var")

        yield from inferred.gen_code(self.CAPTURE_RESULT, Token.GET_VARIABLE)
        yield from self._right.gen_code(self.CAPTURE_RESULT, Token.GET_VARIABLE)

        if self._op.value == "+":
            yield Response(Instr("BINARY_OP", BinaryOp.ADD))

        else:
            raise NotImplementedError(f"Have not implemented operator {self._op.value}")

        if self.INPLACE in intents:
            yield from inferred.gen_code(Token.SET_VARIABLE)

        elif self.IGNORE_RESULT in intents:
            yield Response(Instr("POP_TOP"))

        elif self.CAPTURE_RESULT in intents:
            pass

        else:
            raise Exception(
                f"No relevant intents: Inplace, IGNORE_RESULT, CAPTURE_RESULT passed, ( {intents} )"
            )

    def prepare(self) -> PREPARE_RET:
        yield from self._right.prepare()
