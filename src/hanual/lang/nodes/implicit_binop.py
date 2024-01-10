from __future__ import annotations

from bytecode import Instr, BinaryOp
from typing import TYPE_CHECKING, Any

from hanual.lang.lexer import Token, Generator
from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Response, Request


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

    def gen_code(self, **kwargs: Any) -> Generator[Response | Request, Reply, None]:
        inferred: Token | None = kwargs.get("infer", None)

        if inferred is None:
            raise TypeError(
                f"Argument 'infer' was left blank in '{type(self).__name__}.gen_code'"
            )

        yield from inferred.gen_code(store=False)
        yield from self._right.gen_code(store=False)

        if self._op.value == "+":
            yield Response(Instr("BINARY_OP", BinaryOp.ADD))

        else:
            raise NotImplementedError(f"Have not implemented operator {self._op.value}")

        yield from inferred.gen_code(store=True)

    def prepare(self) -> Generator[Request, Reply, None]:
        yield from self._right.prepare()
