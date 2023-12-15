from __future__ import annotations

from typing import TYPE_CHECKING, Generator

from hanual.lang.nodes.base_node import BaseNode

from hanual.util import Reply, Response, Request


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

    def gen_code(self):
        raise NotImplementedError

    def prepare(self) -> Generator[Response | Request, Reply, None]:
        raise NotImplementedError
