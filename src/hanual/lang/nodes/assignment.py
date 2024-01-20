from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.f_call import FunctionCall
from hanual.lang.util.node_utils import Intent
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.lexer import Token


if TYPE_CHECKING:
    pass


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

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        yield from self._value.gen_code(self.CAPTURE_RESULT)
        yield from self._target.gen_code(Token.SET_VARIABLE)

    def prepare(self) -> PREPARE_RET:
        yield from self._target.prepare()
        yield from self._value.prepare()
