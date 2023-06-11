from __future__ import annotations

from hanual.lang.nodes.base_node import BaseNode
from typing import Union, TYPE_CHECKING
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from .f_call import FunctionCall


class IterLoop(BaseNode):
    def __init__(
        self: BaseNode,
        name: Token,
        iterator: Union[Token, FunctionCall],
    ) -> None:
        self._iterator = iterator
        self._name: Token = name
