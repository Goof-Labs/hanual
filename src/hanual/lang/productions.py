from __future__ import annotations

from typing import TypeVar, Optional, Generic, Union, List, Any, TYPE_CHECKING
from sys import version_info
from abc import ABC

if TYPE_CHECKING:
    from typing_extensions import Self

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class _ProductionInterface(ABC):
    def get(self, *args, **kwargs) -> T:
        pass

    def __format__(self, format_spec: Any) -> None:
        pass


P = TypeVar("P", bound=_ProductionInterface)


class DefaultProduction(_ProductionInterface, ABC, Generic[A, B, C]):
    __slots__ = ("ts",)

    def __init__(self: Self, ts: List[T]) -> None:
        self.ts: List[T] = ts

    @property
    def raw(self: Self) -> List[T]:
        return self.ts

    def __repr__(self: Self) -> str:
        return str(self.ts)

    def __getitem__(self: Self, item: int) -> Union[A, B, C]:
        return self.ts[item]

    def get(self, *args, **kwargs) -> T:
        return super().get(*args, **kwargs)


class ProductionGen(_ProductionInterface, ABC, Generic[A, B, C]):
    """
    This is a genorator production. This is one of many
    productions. Here we get elements out one after the
    other in a genorator like way.
    """

    def __init__(self: Self, tokens: List[T]) -> None:
        self.slice: List[T] = tokens
        self.idx = -1

    def next_token(self: Self) -> T:
        self.idx += 1
        return self.slice[self.idx]

    def back_token(self: Self) -> T:
        self.idx -= 1
        return self.slice[self.idx]

    def peek(self: Self) -> T:
        return self.slice[self.idx]

    def advance_idx(self: Self) -> None:
        self.idx += 1

    def back_idx(self: Self) -> None:
        self.idx -= 1

    def get_token_types(self: Self) -> List[str]:
        return list({t.type for t in self.slice})

    def get_len(self: Self) -> int:
        return len(self.slice)

    def __format__(self: Self, spec: str) -> str:
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
    def __init__(self: Self, tokens: List[T]) -> None:
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

    def __getitem__(self: Self, __key: str) -> T:
        try:
            return self._dct[__key]

        except KeyError as e:
            # only py311+
            if version_info.major >= 3 and version_info.minor >= 11:
                e.add_note(
                    "Could not get key '%s', did you mean one of: %s",
                    (__key, ", ".join(self._dct.keys())),
                )

            else:
                print(
                    "Could not get key '%s', did you mean one of: %s",
                    (__key, ", ".join(self._dct.keys())),
                )
            # display error message
            raise e

    def get(self: Self, key: str, default: Optional[Any] = None) -> None:
        return self._dct.get(key, default)
