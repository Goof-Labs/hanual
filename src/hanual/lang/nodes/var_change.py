from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.lexer import Token
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent
from hanual.util.equal_list import ItemEqualList
from .base_node import BaseNode

if TYPE_CHECKING:
    ...


class VarChange[V: (BaseNode, Token)](BaseNode):
    __slots__ = (
        "_name",
        "_value",
        "_lines",
        "_line_range",
    )

    def __init__(self, name: Token, value: V) -> None:
        self._name: Token = name
        self._value: V = value

    @property
    def name(self) -> Token:
        return self._name

    @property
    def value(self) -> V:
        return self._value

    def gen_code(self, intents: ItemEqualList[Intent], **options) -> GENCODE_RET:
        yield from self._value.gen_code(self.CAPTURE_RESULT)
        yield from self._name.gen_code(Token.SET_VARIABLE)

    def prepare(self) -> PREPARE_RET:
        yield from self._name.prepare()
        yield from self._value.prepare()
