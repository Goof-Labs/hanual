from __future__ import annotations

from .function_wrapper import FunctionWrapper
from contextlib import suppress


class ModuleWrapper:
    def __init__(self) -> None:
        self._exports: dict[str, FunctionWrapper] = {}
        self._name = "<STD-BIN>"

    def __getattribute__(self, __name: str) -> FunctionWrapper:
        with suppress(AttributeError):
            return super().__getattribute__(__name)

        attr = self._exports.get(__name, None)

        if attr:
            return attr

        raise AttributeError(f"{type(self).__name__} has no attr {__name__}, couldn't be found in object or func table")

    def add(self, obj):
        if obj.name in self._exports:
            raise NameError(f"{obj.name!r} has already been defined")

        self._exports[obj.name] = obj

    def __str__(self):
        return f"[ MOD\t{self._name} \n{
            '\n'.join(f"    * {str(k)}\t::\t{str(v)}" for k, v in self._exports.items())
            }]"

    def __repr__(self):
        return str(self)
