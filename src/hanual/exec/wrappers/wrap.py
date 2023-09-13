from __future__ import annotations

from hanual.lang.errors import ErrorType, HanualError, TraceBack
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

    # nothing needs to be changed
    if isinstance(value, LiteralWrapper):
        return res.success(value)

    if isinstance(value, Token):
        if isinstance(value.value, LiteralWrapper):
            return res.success(value.value)

        if value.type == "ID":
            val = scope.get(value.value, None)

            if val is None:
                return res.fail(HanualError(
                    pos=(value.line, value.colm, value.colm+len(value.value)),
                    line=value.line_val,
                    name=ErrorType.unresolved_name,
                    reason=f"Couldn't resolve reference to {value.value!r}",
                    tb=TraceBack(),
                    tip="Did you make a typo?"
                ))

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
