from __future__ import annotations

from typing import TYPE_CHECKING, Generator, NamedTuple, Tuple, TypeVar, Union, Iterable
from hanual.lang.errors import ErrorType, HanualError, TraceBack, Frame
import re

if TYPE_CHECKING:
    from typing_extensions import LiteralString, Literal
    from hanual.exec.wrappers import LiteralWrapper
    from hanual.api.hooks import TokenHook

T = TypeVar("T")


def kw(reg: T) -> Tuple[T, LiteralString]:
    return reg, "kw"


def rx(reg: T) -> Tuple[T, LiteralString]:
    return reg, "rx"


class Token(NamedTuple):
    type: str
    value: Union[str, int, float, LiteralWrapper]
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
                raise ValueError(
                    f"{rule[1][1]!r} is not recognised as a regex or keyword"
                )

    def add_hooks(self, hooks: Iterable[TokenHook]):
        for hook in hooks:
            self._hooks[hook.name] = hook

            if hook.type == "kw":
                self._kwrds.append((hook.name, hook.regex))

            elif hook.type == "rx":
                self._rules.append((hook.name, hook.regex))

            else:
                raise ValueError(
                    f"{hook.type!r} is not recognised as a regex or keyword"
                )

    def tokenize(
        self,
        stream: Generator[str, None, None],
        mode: Literal["exec"] | Literal["compile"],
    ) -> Generator[Token, None, None]:
        # TODO allow rules to ble cleared
        self.update_rules(self.last)

        tok_reg = "|".join("(?P<%s>%s)" % pair for pair in self._rules)

        for line_no, line in enumerate(stream):
            yield from self._tokenize_str(tok_reg, line, line_no, mode=mode)

    def _tokenize_str(
        self,
        tok_reg: str,
        text: str,
        line_no: int,
        mode: Literal["exec"] | Literal["compile"] | Literal["both"] = "both",
    ) -> Generator[Token, None, None]:
        for pat in re.finditer(tok_reg, text):
            kind = pat.lastgroup
            value = pat.group()
            col = pat.start()

            for n, v in self._kwrds:
                if v == value:
                    kind = n

            if kind == "SKIP":
                continue

            if kind == "MISMATCH":
                print(
                    HanualError(
                        pos=(line_no, col, len(value) + col),
                        line=text,
                        name=ErrorType.illegal_character,
                        reason=f"{value!r} is not recognised as a symbol or valid character",
                        tb=TraceBack().add_frame(
                            Frame("Lexing", line_num=line_no, line=text)
                        ),
                        tip=f"try removing that character",
                    ).as_string()
                )
                exit()

            hook = self._hooks.get(kind, None)

            if hook:
                yield hook.gen_token(kind, value, line_no, col, text)
                continue

            elif hasattr(self, f"t_{mode}_{kind}"):
                yield getattr(self, f"t_{mode}_{kind}")(kind, value, line_no, col, text)
                continue

            yield Token(kind, value, line_no, col, text)
