from hanual.lang.productions import DefaultProduction
from hanual.lang.pparser import PParser
from hanual.lang.lexer import Lexer, rx
from typing import NamedTuple


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
    type: str
    name: str


class _RightRegForm(NamedTuple):
    name: str


def make_parser():
    par = PParser()

    @par.rule("LAB SPC CLN ID RAB")
    def form(ts: DefaultProduction, case):
        return _LeftRegForm(ts[1], ts[3])

    @par.rule("LAB ID RAB")
    def form(ts: DefaultProduction, case):
        return _RightRegForm(ts[1])

    return par


class Macro:
    """
    Macros are a mix of regular expressions and well macros, in a nutshel macros are matched with parts of the code, then
    the macros are expanded, this essencially lets the programmers create their own syntax for the language. Regarding the
    regular expressions aspect of the Macro. There are many cases that we need to deal with, we may just want to replace
    the fn keyword with `function`, or just replace a token. This is where a macro type system is neccessery.
     + T -> Token
     + N -> Number
     + I -> Name, Identifier
     + E -> Expression on left
    """

    def __init__(self, pattern: str, target: str) -> None:
        lex = MacroLexer()
        self._pattern = lex.tokenize(pattern)
        self._target = lex.tokenize(target)

    def apply(self, transform: str, lex):
        parser = make_parser()

        print(parser.parse(self._pattern))
        print(parser.parse(self._target))


mac = Macro("<T:left> contains <N:right>", "<right> in <left>")

print(mac.apply("[4, 1234] contains 5"))
