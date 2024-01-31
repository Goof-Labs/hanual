from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from hanual.lang.lexer import Token
from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.block import CodeBlock
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent

if TYPE_CHECKING:
    from hanual.lang.nodes.binop import BinOpNode
    from hanual.lang.nodes.parameters import Parameters
    from hanual.lang.nodes.range_node import RangeNode


class AnonymousFunction(BaseNode, ABC):
    __slots__ = ("_args", "_inner", "fn_name", "_lines", "_line_no", "_return")

    def __init__(
        self, args: Parameters, inner: CodeBlock, ret: Token | BinOpNode | RangeNode
    ) -> None:
        self._inner = inner
        self._args = args
        self._return = ret

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
