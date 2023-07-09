from __future__ import annotations

from hanual.lang.util.class_getattr import ClassGetAttr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self


class RuntimeGlobalState(ClassGetAttr):
    __instance: Self = None

    def __class_getattr__(cls, attr: str):
        if cls.__instance is None:
            cls.__instance = cls()

        return getattr(cls.__instance, attr)

    def __init__(self) -> None:
        self._vars = {}

    def set_var(self, name, value, type):
        ...
