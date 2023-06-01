from __future__ import annotations

from typing import TYPE_CHECKING, Union, List

if TYPE_CHECKING:
    from .constants import UInt, Int, Str


class IR:
    def __init__(self) -> None:
        self._constants: List[Union[UInt, Int, Str]] = []

    def add_const(self, const: Union[UInt, Int, Str]):
        if idx := self.get_const(const):
            return idx

        self._constants.append(const)
        return len(self._constants)

    def get_const(self, const: Union[UInt, Int, Str]):
        try:
            if const.value in (lst := map(lambda x: x.value, self._constants)):
                return list(lst).index(const.value)

        except IndexError:
            return None

    @property
    def add_instruction(self):
        ...
