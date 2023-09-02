from __future__ import annotations


from typing import Dict, TypeVar, Generic, Optional, Any, TYPE_CHECKING
from .base_value import BaseValue

if TYPE_CHECKING:
    from hanual.lang.nodes import StructDefinition
    from hanual.exec.scope import Scope
    from hanual.lang.lexer import Token


_T = TypeVar("_T")


class HlStruct(BaseValue, Generic[_T]):
    __slots__ = "_fields", "_name",

    def __init__(self, struct: StructDefinition = None, _fields: Dict[str, _T] = None, _name: Token = None):
        if struct:
            self._fields: Dict[str, _T] = {field.name: field for field in struct.fields}
            self._name: Token = struct.name

        else:
            self._fields = _fields
            self._name = _name

    def get_field(self, name: str, default: Optional[Any] = None) -> _T:
        return self._fields.get(name, default)

    def set_field(self, name: str, value: _T) -> None:
        self._fields[name] = value

    @classmethod
    def make_instance(cls, name: Token, fields: Dict[str, _T]) -> HlStruct:
        return cls(_fields=fields, _name=name)

    @property
    def name(self) -> Token:
        return self._name

    @property
    def fields(self):
        return self._fields

    def as_string(self, scope: Scope) -> str:
        return f"struct<name={self.name.value!r}>"
