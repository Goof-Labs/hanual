from hanual.lang.productions import DefaultProduction
from hanual.lang.lexer import Lexer, rx, Token
from typing import NamedTuple, Union, List
from hanual.lang.pparser import PParser
from io import StringIO


class MacroLexer(Lexer):
    """
    We also need to lex the macros and eventually parse them to make it easier to work with.
    """

    rules = (
        ("LAB", rx(r"\<")),
        ("RAB", rx(r"\>")),
        ("SPC", rx(r"T|N|I|E")),
        ("CLN", rx(r"\:")),
        ("ID", rx(r"[a-zA-Z_][a-zA-Z0-9_]*")),
        # specials
        ("NEWLINE", rx(r"\n")),
        ("SKIP", rx(r"[ \t]+")),
        ("MISMATCH", rx(r".")),
    )


class _LeftRegForm(NamedTuple):
    type: Token
    name: str


class _RightRegForm(NamedTuple):
    name: str


def make_parser():
    # This is the simplest possible parser
    par = PParser()

    @par.rule("LAB SPC CLN ID RAB")
    def _(ts: DefaultProduction):
        return _LeftRegForm(ts[1], ts[3])

    @par.rule("LAB ID RAB")
    def _(ts: DefaultProduction):
        return _RightRegForm(ts[1])

    return par


class Macro:
    ...
