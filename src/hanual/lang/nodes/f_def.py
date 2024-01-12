from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET

if TYPE_CHECKING:
    from hanual.lang.lexer import Token

    from .block import CodeBlock
    from .parameters import Parameters


class FunctionDefinition(BaseNode):
    __slots__ = (
        "_name",
        "_parameters",
        "_inner",
        "_lines",
        "_line_range",
    )

    def __init__(
        self,
        name: Token,
        params: Parameters,
        inner: CodeBlock,
    ) -> None:
        self._name: Token = name
        self._parameters = params
        self._inner = inner

    @property
    def name(self) -> Token:
        return self._name

    @property
    def arguments(self) -> Parameters:
        return self._parameters

    @property
    def inner(self) -> CodeBlock:
        return self._inner

    def gen_code(self) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
