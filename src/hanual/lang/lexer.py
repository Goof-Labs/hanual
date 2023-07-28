from __future__ import annotations

from typing import NamedTuple, Union, TypeVar, Tuple, Generator, TYPE_CHECKING
import re

if TYPE_CHECKING:
    from typing_extensions import LiteralString

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

    def find_line_num(self, lines: list[str], token: re.Match):
        start, end = token.span()

        # remainder
        rem = start

        for line_num, line in enumerate(lines):
            if len(line) > rem:
                return line_num, line

            else:
                rem -= len(line)

    def tokenize(self, stream: str) -> Generator[Token, None, None]:
        lines = stream.split("\n")
        tok_reg = "|".join("(?P<%s>%s)" % pair for pair in self._rules)

        line_no = 1
        line_start = 0

        for pat in re.finditer(tok_reg, stream):
            kind = pat.lastgroup
            value = pat.group()
            col = pat.start() - line_start

            # print(self.find_line_num(lines, pat))

            for n, v in self._kwrds:
                if v == value:
                    kind = n

            if kind == "NEWLINE":
                line_start = pat.end()
                line_no += 1
                continue

            elif kind == "SKIP":
                continue

            elif kind == "MISMATCH":
                raise Exception

            if hasattr(self, f"t_{kind}"):
                yield getattr(self, f"t_{kind}")(
                    kind, value, line_no, col, lines[line_no - 1]
                )
                continue

            yield Token(kind, value, line_no, col, lines[line_no - 1])
