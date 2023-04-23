from .lexer import Lexer, rx, kw, Token


class HanualLexer(Lexer):
    rules = [
        ("CTX", rx(r"\$[a-zA-Z_][a-zA-Z0-9_]*")),
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
        ("RET", kw("return")),
        ("LET", kw("let")),
        ("VAL", kw("val")),
        ("END", kw("end")),
        ("USE", kw("use")),
        # SYMBOLS
        ("STR", rx(r"(\".*?(?<!\\)(\\\\)*\"|'.*?(?<!\\)(\\\\)*')")),
        ("EL", rx(r"\=\=|\!\=|\>|\<|\<\=|\>\=")),
        ("EQ", rx(r"\=")),
        ("LPAR", rx(r"\(")),
        ("RPAR", rx(r"\)")),
        ("REF", rx(r"\&")),
        ("PIPE", rx(r"\<\|")),
        ("OP", rx(r"[\+\-\\\*]")),
        ("NUM", rx(r"\d+(\.\d*)?")),
        ("COM", rx(r"\,")),
        ("NSA", rx(r"\:\:")),  # name space acesser
        # special cases
        ("NEWLINE", rx(r"\n")),
        ("SKIP", rx(r"[ \t]+|//.*")),
        ("MISMATCH", rx(r".")),
    ]

    def t_NUM(
        self, kind: str, valu: str, line_no: int, col: int, origin_line: str
    ) -> Token:
        return Token(
            kind, float(valu) if "." in valu else int(valu), line_no, col, origin_line
        )