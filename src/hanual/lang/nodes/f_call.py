from __future__ import annotations


from typing import Any, Dict, TYPE_CHECKING, Optional
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from hanual.compile.ir import IR
    from .arguments import Arguments


class FunctionCall(BaseNode):
    def __init__(self: BaseNode, name: Token, arguments: Arguments) -> None:
        self._args: Arguments = arguments
        self._name: Token = name

    def compile(self, ir: IR, to: Optional[str] = None) -> None:
        ir.mov("FP", self._name.value)
        self._args.compile(ir)
        ir.call()

        if not to is None:
            ir.mov(to, "AC")

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def as_dict(self) -> Dict[str, Any]:
        return {"args": self._args.as_dict(), "name": self._name}
