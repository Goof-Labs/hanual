from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.compile.instruction import RET
from hanual.compile.label import Label

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.compile.constant import BaseConstant
    from hanual.lang.lexer import Token

    from .arguments import Arguments
    from .block import CodeBlock


class FunctionDefinition(BaseNode):
    __slots__ = "_name", "_arguments", "_inner"

    def __init__(
        self: FunctionDefinition,
        name: Token,
        args: Arguments,
        inner: CodeBlock,
    ) -> None:
        args.function_def = True

        self._name: Token = name
        self._arguments = args
        self._inner = inner

    @property
    def name(self) -> Token:
        return self._name

    @property
    def arguments(self) -> Arguments:
        return self._arguments

    @property
    def inner(self) -> CodeBlock:
        return self._inner

    def compile(self):
        return [
            Label(self._name.value),  # jump to point
            *self._arguments.compile(),  # put arguments into namespace
            *self._inner.compile(),  # compile block
            RET(None),  # return
        ]

    def get_names(self) -> list[str]:
        return [
            self._name.value,
            *self._arguments.get_names(),
            *self._inner.get_names(),
        ]

    def get_constants(self) -> list[BaseConstant]:
        return self._inner.get_constants()

    def execute(self):
        raise NotImplementedError

    def find_priority(self) -> list[BaseNode]:
        return [self]
