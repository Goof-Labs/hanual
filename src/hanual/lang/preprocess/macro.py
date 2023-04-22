from __future__ import annotations

from typing import NamedTuple, Generator, Optional, Union, List
from hanual.lang.productions import DefaultProduction
from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.lexer import Lexer, rx, Token
from hanual.lang.pparser import PParser


class MacroLexer(Lexer):
    """
    We also need to lex the macros and eventually parse them to make it easier to work with.
    """

    rules = [
        ("LT", rx(r"\<")),
        ("GT", rx(r"\>")),
        ("SPC", rx(r"T|N|I|E")),
        ("CLN", rx(r"\:")),
        ("ARR", rx(r"\-\>")),
        # specials
        *HanualLexer.rules,
    ]


class _LeftRegForm(NamedTuple):
    type: Token
    name: str


class _RightRegForm(NamedTuple):
    name: str


def make_parser():
    # This is the simplest possible parser
    par = PParser()
    found_arrow = False

    @par.rule("LT SPC CLN ID GT")
    def _(ts: DefaultProduction):
        return _LeftRegForm(ts[1], ts[3])

    @par.rule("ARR")
    def _(ts: DefaultProduction):
        if found_arrow:
            raise Exception(
                f"MACRO-ERROR: arrow can't be used twice in one parser {ts[0].line}:{ts[0].colm}"
            )

        return "SPLIT"

    @par.rule("LT ID GT")
    def _(ts: DefaultProduction):
        return _RightRegForm(ts[1])

    return par


class SubstituteMacro:
    """
    NOTE: This macro substituter will only work if, the initial prefix has been removed.

    This is class that will search through the tokens and find specific token patterns and
    replace them. This class will make one parse over
    """

    def __init__(
        self: SubstituteMacro,
        text: str,
        lexer: Optional[HanualLexer] = None,
        parser: Optional[PParser] = None,
    ) -> None:

        assert isinstance(text, str)

        if lexer is None:
            lexer = HanualLexer()

        if parser is None:
            parser = make_parser()

        split = False
        self.right: List[Union[Token, _RightRegForm]] = []
        self.left: List[Union[Token, _LeftRegForm]] = []

        for fragment in parser.parse(lexer.tokenize(text)):
            if fragment == "SPLIT":
                split = True
                continue

            if split:  # aka we are ont he right side of expr
                self.right.append(fragment)

            else:
                self.left.append(fragment)

    def substitute(
        self, ts: Generator[Token, None, None]
    ) -> Generator[Token, None, None]:
        raise NotImplementedError
