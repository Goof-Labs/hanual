from __future__ import annotations

import re
from typing import Generator, Iterable, TYPE_CHECKING

from hanual.lang.errors import ErrorType, Frame, HanualError, TraceBack

from .util.line_range import LineRange
from .token import Token

if TYPE_CHECKING:
    from typing_extensions import LiteralString, Literal
    from hanual.api.hooks import TokenHook


def kw(reg: LiteralString) -> tuple[LiteralString, LiteralString]:
    """Used to define a keyword in the lexer.

    > The function us used with in the lexer. This function lets the user define keywords. For example, if you want to
    > make a keyword called `let` you could use this function.
    >
    > ```py
    > kw("let")
    > ```

    @reg^LiteralString>Name of the keyword.
    | The value of the keyword, e.g. `let`, `if`
    """
    return reg, "kw"


def rx(reg: LiteralString) -> tuple[LiteralString, LiteralString]:
    """Used to define a token in the lexer.

    > The function us used with in the lexer. This function lets the user define patterns/tokens. For example, if you
    > want to make a symbol, `|>` you could use this function with a regular expression that matches the token.
    >
    > ```py
    > rx(r"\\|\\>")
    > ```

    @reg^LiteralString>Value of the regex.
    | The pattern of the token, e.g. [a-zA-Z_][a-zA-Z0-9_]+
    """
    return reg, "rx"


class Lexer:
    __slots__ = "last", "rules", "_rules", "_key_words", "_hooks"

    def __init__(self):
        self._rules = []
        self._key_words = []
        self._hooks: dict[str, TokenHook] = {}
        self.update_rules()

    def update_rules(self, rules=None):
        for rule in self.rules if not rules else rules:
            if rule[1][1] == "kw":
                self._key_words.append((rule[0], rule[1][0]))

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
                self._key_words.append((hook.name, hook.regex))

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

            for n, v in self._key_words:
                if v == value:
                    kind = n

            if kind == "SKIP":
                continue

            if kind == "MISMATCH":
                print(
                    HanualError(
                        pos=LineRange(line_no, line_no),
                        line=text,
                        name=ErrorType.illegal_character,
                        reason=f"{value!r} is not recognised as a symbol or valid character",
                        tb=TraceBack().add_frame(
                            Frame(
                                "Lexing",
                                line=text,
                                line_range=LineRange(start=line_no, end=line_no),
                            )
                        ),
                        tip=f"try removing that character",
                    ).as_string()
                )
                exit()

            hook: TokenHook | None = self._hooks.get(kind, None)

            if hook is not None:
                yield hook.gen_token(
                    kind, value, LineRange(line_no, line_no), col, text
                )

            elif hasattr(self, f"t_{mode}_{kind}"):
                yield getattr(self, f"t_{mode}_{kind}")(kind, value, line_no, col, text)

            else:
                yield Token(
                    token_type=kind,
                    value=value,
                    line_range=LineRange(line_no, line_no),
                    colm=col,
                    lines=text,
                )
