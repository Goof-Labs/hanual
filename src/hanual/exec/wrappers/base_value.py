from __future__ import annotations


from typing import TYPE_CHECKING, Any
from abc import ABC, abstractmethod


if TYPE_CHECKING:
    from hanual.exec.result import Result
    from hanual.exec.scope import Scope


class BaseValue(ABC):
    # for external purposes e.g logging and debugging
    @abstractmethod
    def as_string(self, scope: Scope) -> str:
        raise NotImplementedError

    # internal purposes, str representation of values in the language
    @abstractmethod
    def to_str(self, scope: Scope, x: Any) -> Result:
        raise NotImplementedError

    @abstractmethod
    def get_attr(self, scope: Scope, attr: str) -> Result:
        raise NotImplementedError
