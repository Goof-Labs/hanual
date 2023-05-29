from __future__ import annotations


from typing import TYPE_CHECKING, Any, Dict

from .base_node import BaseNode


if TYPE_CHECKING:
    from hanual.compile.ir import IR
    from .f_call import FunctionCall


class NewStruct(BaseNode):
    def __init__(self: BaseNode, call: FunctionCall) -> None:
        self._call: FunctionCall = call

    @property
    def call(self) -> FunctionCall:
        return self._call

    def compile(self, ir: IR) -> None:
        return super().compile(ir)

    def as_dict(self) -> Dict[str, Any]:
        return super().as_dict()
