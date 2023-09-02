from __future__ import annotations


from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from hanual.exec.scope import Scope


class BaseValue(ABC):
    @abstractmethod
    def as_string(self, scope: Scope) -> str:
        raise NotImplementedError
