from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from bytecode import Instr, Label

from .base_node import BaseNode
from .block import CodeBlock

from hanual.compile.context import Context
from hanual.util import Reply, Response, Request


if TYPE_CHECKING:
    pass


class LoopLoop(BaseNode):
    __slots__ = ("_inner", "_lines", "_line_range")

    def __init__(self, inner: CodeBlock) -> None:
        self._inner: CodeBlock = inner

    @property
    def inner(self) -> CodeBlock:
        return self._inner

    def gen_code(self) -> Generator[Response | Request, Reply, None]:
        context: Context = (yield Request[Context](Request.CREATE_CONTEXT)).response

        start_label = Label()  # for the start of the loop; jumped to if we continue
        end_label = Label()  # end label; jumped to if we break

        with context:
            context.add(parent=self)
            context.add(end_label=end_label)
            context.add(start_label=start_label)

            yield Response(start_label)
            yield from self._inner.gen_code()
            yield Response(Instr("JUMP_BACKWARD", start_label))
            yield Response(end_label)

    def prepare(self) -> Generator[Request, Reply, None]:
        yield from self._inner.prepare()
