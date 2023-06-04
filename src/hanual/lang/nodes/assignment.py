from __future__ import annotations

from hanual.compile.state_fragment import Fragment, MOV, Registers
from typing import TypeVar, Generic, Any, Dict, TYPE_CHECKING
from hanual.lang.errors import Error
from hanual.lang.lexer import Token
from .base_node import BaseNode

if TYPE_CHECKING:
    from hanual.runtime.runtime import RuntimeEnvironment
    from hanual.runtime.status import ExecStatus

T = TypeVar("T", BaseNode, Token)


class AssignmentNode(BaseNode, Generic[T]):
    __slots__ = ("_target", "_value")

    def __init__(self: BaseNode, target: Token, value: T) -> None:
        self._target: Token = target
        self._value: T = value

    @property
    def target(self) -> Token:
        return self._target

    @property
    def value(self) -> T:
        return self._value

    def compile(self) -> None:
        frag = Fragment()

        name_id = frag.add_name(self._target.value)

        if isinstance(self._value, Token):
            if self._value.type == "ID":
                n1 = frag.add_name(self._value.value)
                frag.add_instr(MOV(to=name_id, frm=n1))

            elif self._value.type == "STR":
                val = frag.add_const(self._value.value)
                frag.add_instr(MOV(to=name_id, frm=val))

            elif self._value.type == "NUM":
                val = frag.add_const(self._value.value)
                frag.add_instr(MOV(to=name_id, frm=val))

            else:
                raise NotImplementedError

        else:
            frag.add_frag(self._value.compile())
            frag.add_instr(MOV(to=name_id, frm=Registers.AC))

        return frag

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        return super().execute(rte)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "type": type(self).__name__,
            "name": self._target,
            "value": self._value.as_dict()
            if hasattr(self._value, "as_dict")
            else self._value,
        }
