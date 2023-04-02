from __future__ import annotations


from typing import Any, Tuple, TypeVar
from .base_node import BaseNode


T = TypeVar("T")


class Arguments(BaseNode):
    def __init__(self: BaseNode, *nodes: Tuple[T]) -> None:
        ...

    def compile(self) -> Any:
        return super().compile()

    def eval(self: BaseNode, context) -> Any:
        return super().eval(context)
