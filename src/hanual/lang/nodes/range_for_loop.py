from __future__ import annotations

from typing import TYPE_CHECKING, Self
from bytecode import Label, Instr
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET, GENCODE_INTENTS
from hanual.util.protocalls import Response
from .base_node import BaseNode
from .block import CodeBlock
from .range_node import RangeNode
from hanual.lang.lexer import Token

if TYPE_CHECKING:
    pass


class RangeForLoop(BaseNode):
    __slots__ = (
        "_name",
        "_iterator",
        "_body",
        "_lines",
        "_line_range",
    )

    def __init__(
        self: Self,
        name: Token,
        iterator: RangeNode,
        body: CodeBlock,
    ) -> None:
        self._name = name
        self._body = body
        self._iterator = iterator

    def gen_code(self, intents: GENCODE_INTENTS, **options) -> GENCODE_RET:
        loop_start = Label()
        loop_end = Label()

        yield from self._iterator.gen_code(self.CAPTURE_RESULT)  # sets up iterator
        yield Response(loop_start)
        # get an element from the gen, jump to the end of the loop if exhausted
        yield Response(Instr("FOR_ITER", loop_end))
        # store the iterator
        yield from self._name.gen_code(Token.SET_VARIABLE)

        # loop body
        yield from self._body.gen_code(self.IGNORE_RESULT)

        # go to start of loop to get the next element
        yield Response(Instr("JUMP_BACKWARD", loop_start))

        # cleanup
        yield Response(loop_end)
        yield Response(Instr("END_FOR"))

    def prepare(self) -> PREPARE_RET:
        yield from self._name.prepare()
        yield from self._body.prepare()
        yield from self._iterator.prepare()
