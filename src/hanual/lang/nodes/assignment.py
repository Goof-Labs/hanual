from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.nodes.base_node import BaseNode
from hanual.util import Reply, Request

if TYPE_CHECKING:
    from hanual.compile.context import Context
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

    def gen_code(self, **kwargs):
        with (yield Request[Context](Request.CREATE_CONTEXT)).response as ctx:
            ctx.add(parent=self)

            yield from self._value.gen_code()
            yield from self._target.gen_code(store=True)

    def prepare(self) -> Generator[Request[object], Reply[object] | None, None]:
        yield from self._target.prepare()
        yield from self._value.prepare()
