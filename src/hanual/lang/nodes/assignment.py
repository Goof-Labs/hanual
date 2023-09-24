from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator, Generic, TypeVar

from hanual.compile.constants.constant import Constant
from hanual.compile.instruction import *
from hanual.compile.registers import Registers
from hanual.exec.result import Result
from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack
from hanual.lang.lexer import Token

from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.exec.scope import Scope

T = TypeVar("T", BaseNode, Token)


class AssignmentNode(BaseNode, Generic[T]):
    __slots__ = ("_target", "_value", "_lines", "_line_no")

    def __init__(self: BaseNode, target: Token, value: T, lines: str, line_no: int) -> None:
        self._target: Token = target
        self._value: T = value

        self._line_no = line_no
        self._lines = lines

    @property
    def target(self) -> Token:
        return self._target

    @property
    def value(self) -> T:
        return self._value

    def compile(self):
        if isinstance(self._value, Token):
            if self._value.type == "ID":
                # if we want to allocate one variable to another we make a coppy, this may change at optim time
                return [CPY[self._target.value, self._value.value]]

            elif self._value.type in ("STR", "NUM"):
                # we move a constant into a register
                return [MOV_RC[self._target.value, self._value.value]]

            else:
                raise NotImplementedError

        else:
            return [*self._value.compile(), CPY[self._target.value, Registers.R]]

    def get_constants(self) -> Generator[Constant]:
        # if we want to set the value to a literal, then we add it as a constant
        if isinstance(self._value, Token):
            if self._value.type in ("STR", "NUM"):
                yield Constant(self._value.value)

    def get_names(self) -> list[str]:
        return [self._target.value]

    def execute(self, scope: Scope) -> Result:
        res = Result()

        val = self._get_value(scope, self.value)

        res.inherit_from(val)

        if res.error:
            return res

        scope.set(self.target.value, val.response)

        return res.success(None)

    def _get_value(self, scope: Scope, value: Any) -> Result:
        res = Result()

        if isinstance(value, Token):
            if value.type == "NUM":
                return res.success(value)

            elif value.type == "STR":
                return res.success(value)

            elif value.type == "ID":
                val = scope.get(str(value.value), None)

                if val is None:
                    return res.fail(
                        HanualError(
                            pos=(value.line, value.colm, value.colm + len(value.value)),
                            line=value.line_val,
                            name=ErrorType.unresolved_name,
                            reason=f"Reference to {value.value!r} could not be resolved",
                            tb=TraceBack().add_frame(Frame("Assignment")),
                            tip=f"Did you make a typo?",
                        )
                    )

                return res.success(val)

            else:
                raise NotImplementedError(f"token {value!r} is not recognised")

        else:
            return res.inherit_from(self.value.execute(scope=scope))
