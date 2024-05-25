from __future__ import annotations

from typing import TYPE_CHECKING

from hanual.lang.nodes.base_node import BaseNode
from hanual.lang.nodes.block import CodeBlock
from hanual.lang.util.type_objects import GENCODE_RET, PREPARE_RET
from hanual.lang.util.node_utils import Intent

if TYPE_CHECKING:
    from hanual.lang.nodes.parameters import Parameters


class AnonymousFunction(BaseNode):
    """
    The anonymous function is a function with no name. The function is defined
    like so:

    ```
    """

    __slots__ = ("_args", "_inner", "_lines", "_line_range", "_return")

    def __init__(
        self, args: Parameters,
        inner: CodeBlock,
    ) -> None:
        self._inner = inner
        self._args = args

    def gen_code(self, *intents: Intent, **options) -> GENCODE_RET:
        raise NotImplementedError

    def prepare(self) -> PREPARE_RET:
        raise NotImplementedError
