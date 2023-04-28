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


class LabelHandeler:
    def __init__(self, cls) -> None:
        self._cls = cls

    def new_label(self, name: str = "questionable_identity") -> Label:
        return Label(name=name)
