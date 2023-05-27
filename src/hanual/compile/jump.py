from .label import Label


class Jump:
    def __init__(self, to: Label) -> None:
        self._to = to


class ConditionalJump:
    def __init__(self, to: Label) -> None:
        self._to = to
