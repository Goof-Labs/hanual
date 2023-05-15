from __future__ import annotations

from hanual.compile.assembler import Assembler
from hanual.compile.instruction import *
from .base_node import BaseNode
from .anon_args import AnonArgs
from .block import CodeBlock
from abc import ABC


class AnonymousFunction(BaseNode, ABC):
    __slots__ = ("_args", "_inner", "fn_name")

    def __init__(self: BaseNode, args: AnonArgs, inner: CodeBlock) -> None:
        self._inner = inner
        self._args = args

    def compile(self, global_state: Assembler) -> None:
        fn_start = global_state.add_label()  # no name needed

        self.fn_name = fn_start.mangled_id
        global_state.add_fn_to_table(fn_start.mangled_id, fn_start)

        self._inner.compile(global_state)
