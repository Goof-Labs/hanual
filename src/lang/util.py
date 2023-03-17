from typing import TypeVar


T = TypeVar("T")


class ProductionA:
    def __init__(self, slice):
        self.slice = slice

    def get_token(self) -> T:
        ...
