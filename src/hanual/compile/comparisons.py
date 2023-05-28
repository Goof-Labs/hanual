class Cmp:
    def __init__(self, left, right, op) -> None:
        self._right = right
        self._left = left
        self._op = op

    @property
    def left(self):
        return self._left

    @property
    def op(self):
        return self._op

    @property
    def right(self):
        return self._rigth
