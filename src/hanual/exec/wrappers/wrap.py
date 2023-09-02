from __future__ import annotations

from typing import TypeVar, TYPE_CHECKING
from hanual.exec.result import Result
from hanual.lang.lexer import Token
from .literal import LiteralWrapper

if TYPE_CHECKING:
    from hanual.exec.scope import Scope

_T = TypeVar("_T")


def hl_wrap(scope: Scope, value: _T):
    # TOKENS
    res = Result()

    if isinstance(value, Token):
        if value.type == "ID":
            val = scope.get(value.value, None)

            if val is None:
                return res.fail(f"{value.value!r} can not be resolved")

            return res.success(val)

        elif value.type == "STR":
            return res.success(LiteralWrapper[str](value.value))

        elif value.type == "NUM":
            return res.success(LiteralWrapper[int](value.value))

        else:
            raise NotImplementedError(f"{value} not accounted for")

    elif isinstance(value, int):
        return res.success(LiteralWrapper[int](value))

    # TYPES
    else:
        raise NotImplementedError(f"{type(value).__name__} not accounted for")
