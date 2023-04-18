class ConstantHandeler:
    def __init__(self, cls) -> None:
        self._cls = cls

    def add_const(self, value) -> None:
        self._cls._const_pool.append(value)
        return len(self._cls._const_pool)
