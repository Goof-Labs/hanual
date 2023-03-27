from typing import TypeVar, List, Optional, Any
from abc import ABC


T = TypeVar("T")


class _ProductionInterface(ABC):
    def get(self, *args, **kwargs) -> T:
        raise NotImplementedError

    def __format__(self, format_spec: Any) -> None:
        pass


PInterface = TypeVar("PInterface", bound=_ProductionInterface)


class DefaultProduction(_ProductionInterface, ABC):
    __slots__ = "ts",

    def __init__(self, ts: List[T]) -> None:
        self.ts: List[T] = ts

    def __getitem__(self, item: int) -> T:
        return self.ts[item]


class ProductionGen(_ProductionInterface, ABC):
    """
    This is a genorator production. This is one of many
    productions. Here we get elements out one after the
    other in a genorator like way.
    """

    def __init__(self, tokens: List[T]) -> None:
        self.slice: List[T] = tokens
        self.idx = -1

    def next_token(self) -> T:
        self.idx += 1
        return self.slice[self.idx]

    def back_token(self) -> T:
        self.idx -= 1
        return self.slice[self.idx]

    def peek(self) -> T:
        return self.slice[self.idx]

    def advance_idx(self) -> None:
        self.idx += 1

    def back_idx(self) -> None:
        self.idx -= 1

    def get_token_types(self) -> List[str]:
        return list({t.type for t in self.slice})

    def get_len(self) -> int:
        return len(self.slice)

    def __format__(self, spec: str) -> str:
        """
        '%i' -> index of the production
        '%t' -> current token
        '%l' -> lenght
        '%r' -> raw tokens
        """
        string = ""

        encounter = False
        idx = -1

        while True:
            idx += 1

            try:
                char = spec[idx]

            except IndexError:
                break

            if encounter:
                if char == "i":
                    string += str(self.idx)

                elif char == "t":
                    string += str(self.peek())

                elif char == "l":
                    string += str(self.get_len())

                elif char == "r":
                    string += str(self.slice)

        return string


class ProductionDict(_ProductionInterface):
    def __init__(self, tokens: List[T]) -> None:
        self._dct = {}
        appierence = {}
        # We want to keep track of how many times a token type appieres in total
        # This allows us to do
        # >>> prod.num1
        # >>> prod.num2
        # >>> prod.num3

        for t in tokens:
            if t.type in appierence.items():
                appierences = appierence.get(t.type, 0) + 1

                appierence[t.type] = appierences
                self._dct[f"{t.type.lower()}_{appierences}"] = t
                # We also lower case the token type so the token types look more pythonic

    def __getitem__(self, __key: str) -> T:
        try:
            return self._dct[__key]

        except KeyError as e:
            # only py311+
            e.add_note(
                "Could not get key '%s', did you mean one of: %s",
                (__key, ", ".join(self._dct.keys())),
            )
            # display error message
            raise e

    def get(self, key: str, default: Optional[Any] = None) -> None:
        return self._dct.get(key, default)
