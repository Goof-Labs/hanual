from __future__ import annotations

from typing import NamedTuple, Union, TypeVar, Tuple, Generator
from .errors import HNLIligalCharacterError
import re


T = TypeVar("T")


def kw(reg: T) -> Tuple[T, LiteralString]:
    return reg, "kw"


def rx(reg: T) -> Tuple[T, LiteralString]:
    return reg, "rx"


class Token(NamedTuple):
    type: str
    value: Union[str, int, float]
    line: int
    colm: int
    line_val: str  # The value of the line as a string the token has been extracted from


class Lexer:
    __slots__ = "rules", "_rules", "_kwrds"

    def __init__(self):
        self._rules = []
        self._kwrds = []
        self._update_rules()

    def _update_rules(self, rules=None):
        for rule in self.rules if not rules else rules:
            if rule[1][1] == "kw":
                self._kwrds.append((rule[0], rule[1][0]))

            else:
                self._rules.append((rule[0], rule[1][0]))

    def tokenize(self, stream: str) -> Generator[Token, None, None]:
        lines = stream.split("\n")
        tok_reg = "|".join("(?P<%s>%s)" % pair for pair in self._rules)

        line_no = 1
        line_start = 0

        for pat in re.finditer(tok_reg, stream):
            kind = pat.lastgroup
            valu = pat.group()
            col = pat.start() - line_start

            for n, v in self._kwrds:
                if v == valu:
                    kind = n

            if kind == "NEWLINE":
                line_start = pat.end()
                line_no += 1
                continue

            elif kind == "SKIP":
                continue

            elif kind == "MISMATCH":
                HNLIligalCharacterError().be_raised(
                    sample_code=lines[line_no - 1],
                    line=line_no,
                    col=col,
                    explain=f"{valu!r} was unexpected at this time",
                    stage="LEXING",
                )

            if hasattr(self, f"t_{kind}"):
                yield getattr(self, f"t_{kind}")(
                    kind, valu, line_no, col, lines[line_no - 1]
                )
                continue

            yield Token(kind, valu, line_no, col, lines[line_no - 1])
