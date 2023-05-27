from .label import Label


class Jump:
    def __init__(self, to: Label) -> None:
        self._to: Label = to

    @property
    def to(self) -> Label:
        return self._to


class ConditionalJump:
    def __init__(self, to: Label) -> None:
        self._to: Label = to

    @property
    def to(self) -> Label:
        return self._to
