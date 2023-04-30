from __future__ import annotations


from random import randbytes


class Label:
    def __init__(self, name: str, idx: int = 0) -> None:
        self._mangled = Label.mangle_id(name)
        self._name = name
        self._idx = idx

    @property
    def name(self) -> str:
        return self._name

    @property
    def mangled_id(self) -> str:
        return self._mangled

    @staticmethod
    def mangle_id(name: str) -> str:
        # random.randbytes can return unprintable bytes, also prefix with "_" so we don't need to worry
        # about having a name that starts with a
        return "_" + randbytes(50).hex() + "__" + name

    @property
    def idx(self):
        return self._idx

    def __str__(self):
        return f"Instruction({self.name=} {self.mangled_id=} {self._idx=})"

    def __repr__(self):
        return str(self)
