from __future__ import annotations

from typing import TYPE_CHECKING, Generator, NamedTuple, Tuple, TypeVar, Union, Iterable
from hanual.lang.errors.errors import raise_error
import re


if TYPE_CHECKING:
    from typing_extensions import LiteralString
    from hanual.api.hooks import TokenHook

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
    __slots__ = "last", "rules", "_rules", "_kwrds", "_hooks"

    def __init__(self):
        self._rules = []
        self._kwrds = []
        self._hooks: dict[str, TokenHook] = {}
        self.update_rules()

    def update_rules(self, rules=None):
        for rule in self.rules if not rules else rules:
            if rule[1][1] == "kw":
                self._kwrds.append((rule[0], rule[1][0]))

            elif rule[1][1] == "rx":
                self._rules.append((rule[0], rule[1][0]))

            else:
                raise ValueError(f"{rule[1][1]!r} is not recognised as a regex or keyword")

    def add_hooks(self, hooks: Iterable[TokenHook]):
        for hook in hooks:
            self._hooks[hook.name] = hook

            if hook.type == "kw":
                self._kwrds.append((hook.name, hook.regex))

            elif hook.type == "rx":
                self._rules.append((hook.name, hook.regex))

            else:
                raise ValueError(f"{hook.type!r} is not recognised as a regex or keyword")

    def tokenize(self, stream: Generator[str, None, None]) -> Generator[Token, None, None]:
        tok_reg = "|".join("(?P<%s>%s)" % pair for pair in self._rules + self.last)

        for line_no, line in enumerate(stream):
            yield from self._tokenize_str(tok_reg, line, line_no)

    def _tokenize_str(self, tok_reg: str, text: str, line_no: int):
        for pat in re.finditer(tok_reg, text):
            kind = pat.lastgroup
            value = pat.group()
            col = pat.start()

            for n, v in self._kwrds:
                if v == value:
                    kind = n

            if kind == "SKIP":
                continue

            elif kind == "MISMATCH":
                raise_error(
                    f"{str(line_no).zfill(5)} | {text}",
                    f"unrecognised character '{value}'",
                    "try removing that character",
                )
                exit()

            hook = self._hooks.get(kind, None)

            if hook:
                yield hook.gen_token(kind, value, line_no, col, text)
                continue

            elif hasattr(self, f"t_{kind}"):
                yield getattr(self, f"t_{kind.lower()}")(kind, value, line_no, col, text)
                continue

            yield Token(kind, value, line_no, col, text)
