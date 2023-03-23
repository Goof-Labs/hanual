from typing import NamedTuple
from uuid import uuid4


class Label:
    __slots__ = "_name", "_mangle_name", "_position"

    def __init__(self, name: str, state, mangle: bool = True):
        self._name = name
        self._mangle_name = None

        if mangle:
            self._mangle_name = f"__{uuid4().hex}_{name}"

        self._position = state.position.get()

    @property
    def name(self) -> str:
        return self._name

    @property
    def mangle_name(self) -> str:
        return self._mangle_name

    @property
    def use_name(self) -> str:
        return self._mangle_name or self._name

    @property
    def position(self) -> int:
        return self._position
