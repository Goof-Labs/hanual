from __future__ import annotations


from hanual.lang.lexer import Lexer, rx
from typing import List

# doing string parsing manualy on preprocessers is too much effort, so I am
# basically writing a mini programming language inside a programming language


def generate_lexer(prefix: str, names: List[str]):
    """
    We need to create the lexer inside of this, so we can procedrually add
    our own names, the line labeled "THIS LINE" is especially important,
    it will first create a genorator with the name, and the prefix+name.
    so If our prefix was # and our names where [a b c] the genorator would
    genorate [ (#a , regex( #a ) ) (#b , regex( #b ) ) (#b , regex( #b ) ) ]
    The * would then extract the contense of this list the rules tuple
    this means that if we had some list [ 1 2 3 4 ] and we want to add the
    contense of the list [ 5 6 7 ] to the first list, we could either extend
    the list, so we get [ 1 2 3 4 5 6 ] or we could use the star syntax wich
    would unpack all the elements of this list with the parent list.

    Finally, we just return a `PreProcesserLexer` instance.
    """

    class PreProcesserLexer(Lexer):
        rules = (
            *((name, rx(prefix + name)) for name in names),  # THIS LINE
            ("ID", rx(r"[a-zA-Z_][a-zA-Z0-9_]*")),
            ("EL", rx(r"\=\=|\!\=|\>|\<|\<\=|\>\=")),
            ("NUM", rx(r"\d+(\.\d*)?")),
            ("NEWLINE", rx(r"\n")),
            ("SKIP", rx(r"[ \t]+")),
            ("MISMATCH", rx(r".")),
        )

    return PreProcesserLexer()
