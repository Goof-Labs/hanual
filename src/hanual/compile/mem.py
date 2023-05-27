class Move:
    def __init__(self, to, val) -> None:
        self._val = val
        self._to = to

    @property
    def val(self):
        return self._val

    @property
    def to(self):
        return self._to
