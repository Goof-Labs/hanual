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
    """Implements a binary (arithmatic) operation.

    This node implements arithmatic operations in the language of any two nodes.
    """
    __slots__ = "_right", "_left", "_op", "_lines", "_line_range"

    def __init__(
        self,
        op: Token,
        left: CompilableObject,
        right: CompilableObject,
    ) -> None:
        """Initializes the BinOpNode class.

        Args:
            op (Token): The operator as a token, e.g `+`, `-`.
            left (CompilableObject): The left operator in operang.
            right (CompilableObject): The right operator in operang.
        """
        self._right: CompilableObject = right
        self._left: CompilableObject = left
        self._op: Token = op

    @property
    def left(self) -> CompilableObject:
        """The left operang.

        Returns:
            CompilableObject: The left operang.
        """
        return self._left

    @property
    def right(self) -> CompilableObject:
        """The right operang.

        Returns:
            CompilableObject: The right operang.
        """
        return self._right

    @property
    def op(self) -> Token:
        """The operator.

        Returns:
            Token: The operator as a token.
        """
        return self._op

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        """Genorates the the instructions for the operation.

        The method takes not intentions or options.

        Raises:
            NotImplementedError: If the operator has not been implemented.

        Returns:
            GENCODE_RET: The instructions.
        """
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
                Instr("BINARY_OP", BinaryOp.TRUE_DIVIDE, location=self.get_location())
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
