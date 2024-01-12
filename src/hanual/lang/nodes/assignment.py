from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.util import Request

if TYPE_CHECKING:
    from hanual.lang.lexer import Token


class AssignmentNode[T: BaseNode](BaseNode):
    __slots__ = ("_target", "_value", "_lines", "_line_range")

    def __init__(self, target: Token, value: T) -> None:
        self._target: Token = target
        self._value: T = value

    @property
    def target(self) -> Token:
        return self._target

    @property
    def value(self) -> T:
        return self._value

    def gen_code(self, **kwargs) -> GENCODE_RET:
        reply = yield Request(Request.CREATE_CONTEXT)

        assert reply is not None

        with reply.response as ctx:
            ctx.add(parent=self)
            yield from self._value.gen_code()

            ctx.add(store=True)
            yield from self._target.gen_code()

    def prepare(self) -> PREPARE_RET:
        yield from self._target.prepare()
        yield from self._value.prepare()
