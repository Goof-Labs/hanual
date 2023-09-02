from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING
from hanual.lang.lexer import Token
from .literal import LiteralWrapper


if TYPE_CHECKING:
    from hanual.exec.scope import Scope

_T = TypeVar("_T")


def hl_wrap(scope: Scope, value: _T):
    # TOKENS
    if isinstance(value, Token):
        if value.type == "ID":
            return scope.get(value.value, None)

        elif value.type == "STR":
            return LiteralWrapper[str](value.value)

        elif value.type == "INT":
            return LiteralWrapper[int](value.value)

        else:
            raise NotImplementedError(f"{value} not accounted for")

    # TYPES
    else:
        raise NotImplementedError(f"{type(value).__name__} not accounted for")
