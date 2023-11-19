class LiteralWrapper[T]:
    def __init__(self, value: T) -> None:
        self._value: T = value

    @property
    def value(self) -> T:
        return self._value
