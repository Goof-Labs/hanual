from __future__ import annotations

import re
from typing import TYPE_CHECKING, Generator, Iterable, Literal, LiteralString

from hanual.errors.error import HanualSyntaxError
from .util.line_range import LineRange
from .token import Token


def kw(reg: LiteralString) -> tuple[LiteralString, LiteralString]:
    """Used to define a keyword in the lexer.

    The function us used with in the lexer. This function lets the user define keywords. For example, if you want to
    make a keyword called `let` you could use this function.

    >>> ```
    >>> kw("let")
    >>> ```
    """
    return reg, "kw"


def rx(reg: LiteralString) -> tuple[LiteralString, LiteralString]:
    """Used to define a token in the lexer.

    The function us used with in the lexer. This function lets the user define patterns/tokens. For example, if you
    want to make a symbol, `|>` you could use this function with a regular expression that matches the token.
    
    >>> ```
    >>> rx(r"\\|\\>")
    >>> ```
    """
    return reg, "rx"


class Lexer:
    __slots__ = "last", "rules", "_rules", "_key_words"

    """A class that lazily performs lexical analysis on a piece of text.

    Raises:
        ValueError: Occurs when a token is identified as neither a keyword or regex.
        ValueError: Occurs when a token is identified as neither a keyword or regex.
        Exception: The provided token type was "None"
    """

    __slots__ = "last", "rules", "_rules", "_key_words", "_hooks"

    def __init__(self):
        self._rules = []
        self._key_words = []
        self.update_rules()

    def update_rules(self, rules: Iterable[tuple[str, str]]=None):
        """Categorises the class's rules and updates them.

        Args:
            rules (Iterable[tuple[str]], optional): The rules that are going to be added to the lexer. Defaults to None.

        Raises:
            ValueError: The token can't be identified as being a keyword 'kw' or regex 'rk'.
        """

        for rule in self.rules if not rules else rules:
            if rule[1][1] == "kw":
                self._key_words.append((rule[0], rule[1][0]))

            elif rule[1][1] == "rx":
                self._rules.append((rule[0], rule[1][0]))

            else:
                raise ValueError(
                    f"{rule[1][1]!r} is not recognised as a regex or keyword"
                )

    def tokenize(
        self,
        stream: Generator[str, None, None],
        mode: Literal["exec"] | Literal["compile"],
    ) -> Generator[Token, None, None]:
        """Tokenizes the passed string into the tokens in the class.

        Args:
            stream (Generator[str, None, None]): The text to be tokenized (input should be lines of code).
            mode (Literal[&quot;exec&quot;] | Literal[&quot;compile&quot;]): The compiler mode.

        Yields:
            Generator[Token, None, None]: The pipeline of tokens.
        """
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
        """Does the behind-the-sceens tokenization of the text.

        Args:
            tok_reg (str): The regular expression of all language tokens.
            text (str): The line of code to be analysed.
            line_no (int): The line number of the source code.
            mode (Literal[&quot;exec&quot;] | Literal[&quot;compile&quot;] | Literal[&quot;both&quot;], optional): The compiler mode. Defaults to "both".

        Raises:
            Exception: When the current token type is None.

        Yields:
            Generator[Token, None, None]: The token stream.
        """
        for pat in re.finditer(tok_reg, text):
            kind = pat.lastgroup
            value = pat.group()
            col = pat.start()

            for n, v in self._key_words:
                if v == value:
                    kind = n

            if kind == "SKIP":
                continue

            if kind is None:
                raise Exception("kind is None")

            if kind == "MISMATCH":
                HanualSyntaxError(
                    line_str=text,
                    line_range=LineRange(line_no, line_no),
                    hint=f"Character {value!r} is not a recognised character"
                ).display()

            # create the token
            if hasattr(self, f"t_{mode}_{kind}"):
                yield getattr(self, f"t_{mode}_{kind}")(kind, value, line_no, col, text)

            else:
                yield Token(
                    token_type=kind,
                    value=value,
                    line_range=LineRange(line_no, line_no),
                    colm=col,
                    lines=text,
                )
