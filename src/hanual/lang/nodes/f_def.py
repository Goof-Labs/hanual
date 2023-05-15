from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from hanual.compile import Assembler
    from .arguments import Arguments
    from .block import CodeBlock


class FunctionDefinition(BaseNode):
    __slots__ = "_name", "_arguments", "_inner"

    def __init__(
        self: FunctionDefinition, name: Token, args: Arguments, inner: CodeBlock
    ) -> None:
        self._name: Token = name
        self._arguments = args
        self._inner = inner

    def compile(self, global_state: Assembler) -> Any:
        label = global_state.add_label(self._name.value)
        global_state.add_function(label)

        self._arguments.compile(global_state)
        self._inner.compile(global_state)

        # TODO Add returning

        global_state.add_fn_to_table(self._name, label)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "args": self._arguments.as_dict(),
            "name": self._name,
            "inner": self._inner.as_dict()
            if hasattr(self._inner, "as_dict")
            else self._inner,
        }
