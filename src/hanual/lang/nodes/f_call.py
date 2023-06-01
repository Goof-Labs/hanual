from __future__ import annotations


from typing import Any, Dict, TYPE_CHECKING, Optional, Union
from .dot_chain import DotChain
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from .arguments import Arguments


class FunctionCall(BaseNode):
    def __init__(self: BaseNode, name: Token, arguments: Arguments) -> None:
        self._name: Union[Token, DotChain] = name
        self._args: Arguments = arguments

    def compile(self) -> None:
        raise NotImplementedError

    @property
    def name(self) -> Token:
        return self._name

    @property
    def args(self) -> Arguments:
        return self._args

    def as_dict(self) -> Dict[str, Any]:
        return {"args": self._args.as_dict(), "name": self._name}
