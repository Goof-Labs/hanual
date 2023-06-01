from __future__ import annotations


from typing import Any, Dict, Union, List, TYPE_CHECKING
from hanual.lang.lexer import Token
from typing_extensions import Self
from .base_node import BaseNode

if TYPE_CHECKING:
    ...


class DotChain(BaseNode):
    def __init__(self: BaseNode) -> None:
        self._chain: List[Token] = []

    def add_name(self, name: Union[Token, DotChain]) -> Self:
        if isinstance(name, Token):
            self._chain.insert(0, name)

        elif isinstance(name, DotChain):
            self._chain = [*self._chain, *name.chain]

        else:
            raise Exception

        return self

    @property
    def chain(self) -> List[Token]:
        return self._chain

    def compile(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
