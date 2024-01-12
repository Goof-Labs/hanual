from __future__ import annotations

from typing import TYPE_CHECKING

from bytecode import Instr, Label

from hanual.compile.context import Context
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.util import Request, Response

from .base_node import BaseNode
from .block import CodeBlock

if TYPE_CHECKING:
    pass


class LoopLoop(BaseNode):
    __slots__ = ("_inner", "_lines", "_line_range")

    def __init__(self, inner: CodeBlock) -> None:
        self._inner: CodeBlock = inner

    @property
    def inner(self) -> CodeBlock:
        return self._inner

    def gen_code(self) -> GENCODE_RET:
        reply = yield Request(Request.CREATE_CONTEXT)

        assert reply is not None
        assert isinstance(reply.response, Context)

        start_label = Label()  # for the start of the loop; jumped to if we continue
        end_label = Label()  # end label; jumped to if we break

        with reply.response as ctx:
            ctx.add(parent=self)
            ctx.add(end_label=end_label)
            ctx.add(start_label=start_label)

            yield Response(start_label)
            yield from self._inner.gen_code()
            yield Response(Instr("JUMP_BACKWARD", start_label))
            yield Response(end_label)

    def prepare(self) -> PREPARE_RET:
        yield from self._inner.prepare()
