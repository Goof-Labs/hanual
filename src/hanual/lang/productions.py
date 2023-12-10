from __future__ import annotations

from typing import TYPE_CHECKING, List, Self
from warnings import warn_explicit
import inspect


if TYPE_CHECKING:
    from hanual.lang.nodes.base_node import BaseNode
    from hanual.lang.lexer import Token


class DefaultProduction[T: Token | BaseNode]:
    __slots__ = ("ts",)

    def __init__(self: Self, ts: List[T], **kwargs) -> None:
        self.ts: List[T] = ts

        if kwargs:
            func_ln = inspect.getfile(kwargs["fn"])
            warn_explicit(
                message=f"Default production was passed too many arguments",
                category=UserWarning,
                filename=func_ln,
                lineno=kwargs["fn"].__code__.co_firstlineno
            )

    def __repr__(self: Self) -> str:
        return str(self.ts)

    def __getitem__(self: Self, item: int) -> T:
        return self.ts[item]
