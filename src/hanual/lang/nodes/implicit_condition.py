from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

from hanual.compile.constants.constant import Constant
from hanual.exec.result import Result
from hanual.exec.wrappers import hl_wrap
from hanual.exec.wrappers.literal import LiteralWrapper
from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack
from hanual.lang.lexer import Token

from .base_node import BaseNode
from .f_call import FunctionCall

if TYPE_CHECKING:
    from hanual.exec.scope import Scope


class ImplicitCondition(BaseNode):
    def __init__(self, op: Token, val: Union[Token, FunctionCall]) -> None:
        self._val: Union[Token, FunctionCall] = val
        self._op: Token = op

    @property
    def value(self) -> Union[Token, FunctionCall]:
        return self._val

    @property
    def op(self) -> Token:
        return self._op

    def compile(self, name: str):
        # These conditions are implicit and require the context from the parent node to
        # guess what it should compare against
        return []

    def get_constants(self) -> list[Constant]:
        if isinstance(self._val, Token):
            if self._val.type in ("STR", "NUM"):
                yield Constant(self._val.value)

    def get_names(self) -> list[str]:
        if isinstance(self._val, Token):
            if self._val.type == "ID":
                return [Constant(self._val.value)]

        return []

    def execute(self, scope: Scope, name: Optional[str] = None) -> Result:
        # get left side
        if name is None:
            raise Exception(f"'name' was not passed as an argument")

        val = scope.get(name, None)

        if val is None:
            return Result().fail(
                HanualError(
                    pos=(
                        self._op.line,
                        self._op.colm,
                        self._op.colm + len(self._op.value),
                    ),
                    line=self._op.line_val,
                    name=ErrorType.unresolved_name,
                    reason=f"Couldn't resolve reference to {self._op.value!r}",
                    tb=TraceBack().add_frame(Frame("implicit condition")),
                    tip="Did you make a typo?",
                )
            )

        # get right side
        if isinstance(self._val, FunctionCall):
            other = self._val.execute(scope=scope)

        else:
            other = hl_wrap(scope, self._val)

        if other is None:
            raise Exception

        other = other.response.value

        if isinstance(val, LiteralWrapper):
            val = val.value

        # check and do conditions
        if self._op.value == "==":
            return Result().success(val == other)

        elif self._op.value == ">":
            return Result().success(val > other)

        elif self._op.value == "<":
            return Result().success(val < other)

        elif self._op.value == ">=":
            return Result().success(val >= other)

        elif self._op.value == "<=":
            return Result().success(val <= other)

        elif self._op.value == "!=":
            return Result().success(val > other)

        raise Exception(f"{self._op} not accounted for")
