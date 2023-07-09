from __future__ import annotations

from hanual.lang.util.class_getattr import ClassGetAttr


class GlobalState(ClassGetAttr):
    def __class_getattr__(cls, attr: str):
        ...
