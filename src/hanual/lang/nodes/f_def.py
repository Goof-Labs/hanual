from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from hanual.compile.constant import Constant
from hanual.lang.errors import Error
from hanual.lang.nodes.base_node import BaseNode
from hanual.runtime.runtime import RuntimeEnvironment
from hanual.runtime.status import ExecStatus
from hanual.compile.label import Label
from hanual.compile.instruction import RET
from .base_node import BaseNode

if TYPE_CHECKING:
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

    def compile(self) -> None:
        return [
            Label(self._name.value), # jump point
            *self._arguments.compile(), # put arguments into namespace
            *self._inner.compile(), # compile block
            RET(None), # return
        ]

    def get_names(self) -> list[str]:
        names = []

        names.append(self._name.value)
        names.extend(self._arguments.get_names())
        names.extend(self._inner.get_names())

        return names

    def get_constants(self) -> list[Constant]:
        return self._inner.get_constants()

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def find_priority(self) -> list[BaseNode]:
        return [self]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "args": self._arguments.as_dict(),
            "name": self._name,
            "inner": self._inner.as_dict()
            if hasattr(self._inner, "as_dict")
            else self._inner,
        }
