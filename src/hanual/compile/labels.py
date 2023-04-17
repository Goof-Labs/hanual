from random import randbytes
from . import GlobalState


class Label:
    def __init__(self, addr: int, name: str) -> None:
        self._mangeled = Label.mangle_id(name)
        self._adress = addr
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def position(self) -> str:
        return self._adress

    @property
    def mangeled_id(self) -> str:
        return self._mangeled

    @property
    def address(self) -> None:
        return self._adress

    @staticmethod
    def mangle_id(name: str) -> str:
        # random.randbytes can return unprintable bytes, also prefix with "_" so we don't need to worry
        # about having a name that starts with a
        return "_" + randbytes(50).hex() + "__" + name


class LabelHandeler:
    def __init__(self, cls: GlobalState) -> None:
        self._cls = cls

    def new_label(self, name: str = "questionable_identity") -> None:
        self._cls.advance()
        return Label(addr=self._cls.position, name=name)
