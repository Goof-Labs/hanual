from typing import TypeVar, List, LiteralString


T = TypeVar("T")


class ProductionGen:
    def __init__(self, tokens: List[T]) -> None:
        self.slice: List[T] = tokens
        self.idx = -1

    def get_token(self) -> T:
        self.idx += 1
        return self.slice[self.idx]

    def get_token_types(self) -> List[str]:
        return list({t.type for t in self.slice})

    def get_len(self) -> int:
        return len(self.slice)


class ProductionMangle:
    def __init__(self, tokens: List[T]) -> None:
        self.tokens
