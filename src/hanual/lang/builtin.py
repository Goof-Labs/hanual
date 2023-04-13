from .lexer import Lexer, rx, kw, Token


class HanualLexer(Lexer):
    rules = [
        ("ID", rx(r"[a-zA-Z_][a-zA-Z0-9_]*")),
        ("SHOUT", kw("SHOUT")),
        # KEYWORDS
        ("FN", kw("fn")),
        ("IF", kw("if")),
        ("ITR", kw("iter")),
        ("WHL", kw("while")),
        ("FOR", kw("for")),
        ("EIF", kw("elif")),
        ("ELSE", kw("else")),
        ("FREEZE", kw("freeze")),
        ("LET", kw("let")),
        ("VAL", kw("val")),
        ("END", kw("end")),
        # SYMBOLS
        ("STR", rx(r"\".*?\"")),
        ("EL", rx(r"\=\=|\!\=|\>|\<|\<\=|\>\=")),
        ("EQ", rx(r"\=")),
        ("LPAR", rx(r"\(")),
        ("RPAR", rx(r"\)")),
        ("REF", rx(r"\&")),
        ("PIPE", rx(r"\<\|")),
        ("OP", rx(r"[\+\-\\\*]")),
        ("NUM", rx(r"\d+(\.\d*)?")),
        ("COM", rx(r"\,")),
        # special cases
        ("NEWLINE", rx(r"\n")),
        ("SKIP", rx(r"[ \t]+|\\*.*\\")),
        ("MISMATCH", rx(r".")),
    ]

    def t_NUM(self, kind: str, valu: str, line_no: int, col: int) -> Token:
        return Token(kind, float(valu) if "." in valu else int(valu), line_no, col)
