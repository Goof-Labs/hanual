from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Self
from warnings import warn_explicit

if TYPE_CHECKING:
    from hanual.lang.lexer import Token
    from hanual.lang.nodes import BaseNode


class DefaultProduction[T: Token | BaseNode]:
    __slots__ = ("ts",)

    def __init__(self: Self, ts: list[T], **kwargs) -> None:
        self.ts: list[T] = ts

        if kwargs:
            func_ln = inspect.getfile(kwargs["fn"])
            warn_explicit(
                message=f"Default production was passed too many arguments",
                category=UserWarning,
                filename=func_ln,
                lineno=kwargs["fn"].__code__.co_first_line_no,
            )

    def __repr__(self: Self) -> str:
        return str(self.ts)

    def __getitem__(self: Self, item: int) -> T:
        return self.ts[item]
