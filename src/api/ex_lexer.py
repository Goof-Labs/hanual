from __future__ import annotations

from typing import TypeVar, Union, List, Tuple, LiteralString
from abc import ABC, abstractmethod
from ..lang.lexer import Lexer
from enum import Enum
import sys


T = TypeVar("T")


class _RuleInterface(ABC):
    @abstractmethod
    def get_rules(self) -> List[Tuple[LiteralString, Tuple[T, LiteralString]]]:
        """
        This should return a list containing tuples with a
        string and another tuple with a regex pattern and
        type. I have abstracted some parts of the type for
        the convenience of the user.

        To abstract away the nested tuple you can use either
        the `kw` or `rx` function. These will return the
        inputted value and "rx" or "kw", these can either
        be explicitly used or the function can be used. This
        would help the lexer to differentiate between a
        keyword and a regex pattern which is what the other
        one is. This means that the user just needs to specify.

        >>> # Implementation of functions
        >>> def rx(n): return n, "rx"
        >>> def kw(n): return n, "kw"
        >>>
        >>> [
        ...     ("NAME", rx("some_regex_pattern")),
        ...     ("CRAP", kw("crap_keyword"))
        ... ]
        """
        raise NotImplementedError


AttrBound = TypeVar("AttrBound", bound=_RuleInterface)
EnumBound = TypeVar("EnumBound", bound=Enum)


class ExtendableLexer:
    __slots__ = "_lex"

    def __init__(self: ExtendableLexer):
        self._lex = Lexer()

    def add_rules(self: ExtendableLexer, obj: Union[EnumBound, T]) -> None:
        arr: List = []

        if isinstance(type(obj), Enum):
            obj: EnumBound

            val: Tuple[..., str]
            name: str

            for name, val in obj.__members__.keys():
                arr.append((name, val))

        elif hasattr(obj, "get_rules"):
            res: List[Tuple[str, Tuple[..., str]]] = obj.get_rules()

            if not self._proof_read(res):
                # mismatch
                raise ValueError(
                    "%s returned wrong type expected list[tuple[str, (str, 'kw' | 'rx')]]",
                    (type(obj).__name__,),
                )

            arr.extend(res)

        else:
            err: AttributeError = AttributeError("NOTE: %s has no attribute", (type(obj).__name__,))

            # error.add_note() was only added in py 311
            if sys.version_info.minor >= 11:
                err.add_note("NOTE: you may want to add an 'get_rules' function")

            raise err

        self._lex._update_rules(arr)

    def _get(self: ExtendableLexer) -> Lexer:
        return self._lex

    @staticmethod
    def _proof_read(inp) -> bool:
        """
        This will check if the input conforms to the following type

        [
            (str, (str, "rx" | "kw")),
            ...
        ]

        """
        if not isinstance(inp, list):
            return False

        for k, v in inp:
            if not isinstance(k, str):
                return False

            if not isinstance(v, tuple):
                return False

            if not (v[1] == "kw" or v[1] == "rx"):
                return False

            if not isinstance(v[0], str):
                return False

        return True
