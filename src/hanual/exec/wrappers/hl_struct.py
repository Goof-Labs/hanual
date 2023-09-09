from __future__ import annotations

from hanual.exec.hl_builtin.base_builtin import HlWrapperFunction
from hanual.lang.errors.errors import ErrorType, HanualError
from hanual.exec.wrappers.literal import LiteralWrapper
from typing import Dict, Optional, Any, TYPE_CHECKING
from hanual.lang.errors.trace_back import TraceBack
from hanual.exec.result import Result
from .base_value import BaseValue
from abc import ABC

if TYPE_CHECKING:
    from hanual.lang.nodes import StructDefinition, StrongField
    from hanual.exec.scope import Scope
    from hanual.lang.lexer import Token


class HlStruct(BaseValue, ABC):
    __slots__ = "_fields", "_name", "_base",

    def __init__(self, struct: StructDefinition = None, _fields: Dict[Token, Any] = None, _name: Token = None):

        if struct:
            self._fields: Dict[str, Any] = {field.name: field for field in struct.fields}
            self._name: Token = struct.name

            self._base = True

        else:
            self._base = False

            self._fields = {k.value: LiteralWrapper(None) for k, v in _fields.items()}
            self._name = _name

    def get_field(self, name: str, default: Optional[Any] = None) -> Any:
        if self._base:  # dealing with raw struct, not an instance
            raise Exception
        return self._fields.get(name, default)

    def set_attr(self, name: Token, value: Any) -> Result:
        if name.value in self._fields:
            self._fields[name.value] = value
            return Result().success(None)

        return Result().fail(HanualError(
            pos=None,
            line=None,
            name=ErrorType.cant_set_attr,
            reason=f"can't set attribute {name!r} on {self._name.value}",
            tb=TraceBack(),
            tip=f"Did you make a typo",
        ))

    def get_attr(self, attr: str, scope: Optional[Scope] = None) -> Result:
        from hanual.lang.nodes.parameters import Parameters
        from hanual.exec.wrappers import hl_wrap

        res = Result()

        # if the struct is a template
        if self._base:
            val: StrongField = self.get_field(attr, None)

            if val is None:
                return res.fail(HanualError(
                    pos=None,
                    line=None,
                    name=ErrorType.attr_not_found,
                    reason=f"Attribute {self._name.value}.{attr} could not be resolved",
                    tb=TraceBack(),
                    tip="did you make a typo",
                ))

            val = hl_wrap(scope=scope, value=val.name)
            return res.success(val)

        else:
            # check what values the struct is storing
            val: LiteralWrapper = self.get_field(attr, None)

            if val is None:
                # check if the attr are specific properties

                if attr == "to_str":
                    return Result().success(
                        HlWrapperFunction(name="to_str", params=Parameters([]), func=self.to_str))

                    # error if all fails
                return res.fail(HanualError(
                        pos=None,
                        line=None,
                        name=ErrorType.attr_not_found,
                        reason=f"Attribute {self._name.value}.{attr} could not be resolved",
                        tb=TraceBack(),
                        tip="did you make a typo",
                    ))

        if val.value is None:  # default, not set
            return res.fail(HanualError(
                pos=(self._name.line, self._name.colm, self._name.colm+len(self._name.value)),
                line=self._name.line_val,
                name=ErrorType.non_initialized_value,
                reason=f"The value of {self._name.value}.{attr} has not been initialized",
                tb=TraceBack(),
                tip=f"Make sure all values have been initialized",
            ))

        return res.success(val)

    @classmethod
    def make_instance(cls, name: Token, fields: Dict[Token, Any]) -> HlStruct:
        return cls(_fields=fields, _name=name)

    @property
    def name(self) -> Token:
        return self._name

    @property
    def fields(self):
        return self._fields

    def as_string(self, scope: Scope) -> str:
        return f"struct<name={self.name.value!r}>"

    def to_str(self, scope: Scope, args: Dict[str, Any]) -> Result:
        return Result().success(LiteralWrapper(self.as_string(scope)))
