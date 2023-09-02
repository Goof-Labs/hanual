from __future__ import annotations


from typing import Dict, TypeVar, Generic, Optional, Any, TYPE_CHECKING
from .base_value import BaseValue

if TYPE_CHECKING:
    from hanual.lang.nodes import StructDefinition
    from hanual.exec.scope import Scope
    from hanual.lang.lexer import Token


_T = TypeVar("_T")


class HlStruct(BaseValue, Generic[_T]):
    def __init__(self, struct: StructDefinition):
        self._fields: Dict[str, _T] = {field.name: field for field in struct.fields}
        self._name: Token = struct.name

    def get_field(self, name: str, default: Optional[Any] = None) -> _T:
        return self._fields.get(name, default)

    def set_field(self, name: str, value: _T) -> None:
        self._fields[name] = value

    @property
    def name(self) -> Token:
        return self._name

    def as_string(self, scope: Scope) -> str:
        return f"struct<name={self.name.value!r}>"
