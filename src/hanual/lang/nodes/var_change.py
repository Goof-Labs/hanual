from __future__ import annotations

from hanual.lang.errors import HanualError, ErrorType, Frame, TraceBack
from hanual.compile.constants.constant import Constant
from hanual.lang.nodes.dot_chain import DotChain
from hanual.compile.registers import Registers
from typing import TYPE_CHECKING, TypeVar
from hanual.compile.instruction import *
from hanual.exec.result import Result
from hanual.lang.lexer import Token
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.exec.scope import Scope

T = TypeVar("T", bound=BaseNode)


class VarChange(BaseNode):
    __slots__ = "_name", "_value",

    def __init__(self: BaseNode, name: Token, value) -> None:
        self._name: Token = name
        self._value: T = value

    @property
    def name(self) -> Token:
        return self._name

    @property
    def value(self) -> T:
        return self._value

    def compile(self):
        instructions = []

        if isinstance(self._value, Token):
            if self._value.type in ("STR", "NUM"):
                instructions.append(
                    MOV_RC[self._name.value, Constant(self._value.value)]
                )

            elif self._value.type == "NME":
                instructions.append(CPY[self._name.value, self._value.value])

            else:
                raise NotImplementedError

        else:
            instructions.extend(self._value.compile())
            instructions.append(MOV_RR[self._name.value, Registers.R])

        return instructions

    def _get_value(self, scope: Scope) -> Result:
        res = Result()

        # is the name a token?
        if isinstance(self._value, Token):
            if self._value.type in ("STR", "NUM"):  # a literal
                return res.success(self._value)

            elif self._name.type == "ID":
                val = scope.get(self._value.value, None)

                if val is None:
                    return res.fail(HanualError(
                        pos=(self._name.line, self._name.colm, self._name.colm + len(self._name.value)),
                        line=self._name.line_val,
                        name=ErrorType.unresolved_name,
                        reason=f"Couldn't resolve reference to {self._name.value!r}",
                        tb=TraceBack().add_frame(Frame("new struct")),
                        tip="Did you make a typo?"
                    ))

                return res.success(val)

            else:
                raise Exception
        # should be executable
        val, err = res.inherit_from(self._value.execute(scope))

        if err:
            return res.fail(err.add_frame(Frame("var change")))

        return res.success(val)

    def execute(self, scope: Scope) -> Result:
        res: Result = Result()

        # get the name
        if isinstance(self._name, Token):
            # the variable does not exist
            if not scope.exists(self._name.value):
                return res.fail(HanualError(
                    pos=(self._name.line, self._name.colm, self._name.colm + len(self._name.value)),
                    line=self._name.line_val,
                    name=ErrorType.unresolved_name,
                    reason=f"Couldn't resolve reference to {self._name.value!r}",
                    tb=TraceBack().add_frame(Frame("new struct")),
                    tip="Did you make a typo?"
                ))
            # get the value
            val, err = res.inherit_from(self._get_value(scope))

            if err:
                return res.fail(err.add_frame("var change"))

            scope.set(self._name.value, val)
            return res.success(None)

        elif isinstance(self._name, DotChain):
            # dot chain

            val, err = res.inherit_from(self._get_value(scope))

            if err:
                return res.fail(err.add_frame(Frame("var change")))

            _, err = res.inherit_from(self._name.execute(scope, set_attr=val))

            if err:
                return res.fail(err.add_frame(Frame("var change")))

        return res.success(None)

    def get_constants(self) -> list[Constant]:
        consts = []

        if isinstance(self._value, Token):
            if self._value.type in ("STR", "NUM"):
                consts.append(Constant(self._value.value))

        else:
            consts.extend(self._value.get_constants())

        return consts

    def get_names(self) -> list[str]:
        return [
            self._name.value,
            *self._value.get_names()
        ]

    def find_priority(self) -> list[BaseNode]:
        # TODO take blocks or lambda functions into account
        return []
