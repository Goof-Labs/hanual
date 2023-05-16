from __future__ import annotations


from .lexer import Lexer, rx, kw, Token


class HanualLexer(Lexer):
    rules = [
        # NAMES
        ("CTX", rx(r"\$[a-zA-Z_][a-zA-Z0-9_]*")),
        ("ID", rx(r"[a-zA-Z_][a-zA-Z0-9_]*")),
        ("ADT", rx(r"\\[a-zA-Z0-9_]+")),  # algebraic datatype \name
        # KEYWORDS
        ("SHOUT", kw("SHOUT")),
        ("FN", kw("fn")),
        ("AS", kw("as")),
        ("IF", kw("if")),
        ("DO", kw("do")),
        ("ITR", kw("iter")),
        ("WHL", kw("while")),
        ("FOR", kw("for")),
        ("LOOP", kw("loop")),
        ("BREAK", kw("break")),
        ("FREEZE", kw("freeze")),
        ("RET", kw("return")),
        ("LET", kw("let")),
        ("END", kw("end")),
        ("USE", kw("use")),
        # SYMBOLS
        ("STR", rx(r"(\".*?(?<!\\)(\\\\)*\"|'.*?(?<!\\)(\\\\)*')")),
        ("EL", rx(r"\=\=|\!\=|\>|\<|\<\=|\>\=")),
        ("EQ", rx(r"\=")),
        ("LPAR", rx(r"\(")),
        ("RPAR", rx(r"\)")),
        ("OP", rx(r"[\+\-\\\*]")),
        ("NUM", rx(r"\d+(\.\d+)?")),
        ("COM", rx(r"\,")),
        ("NSA", rx(r"\:\:")),  # name space access
        ("DOT", rx(r"\.")),
        ("LSB", rx(r"\[")),
        ("RSB", rx(r"\]")),
        # special cases
        ("NEWLINE", rx(r"\n")),
        ("SKIP", rx(r"[ \t]+|//.*")),
        ("MISMATCH", rx(r".")),
    ]

    def t_NUM(
        self, kind: str, value: str, line_no: int, col: int, origin_line: str
    ) -> Token:
        return Token(
            kind,
            float(value) if "." in value else int(value),
            line_no,
            col,
            origin_line,
        )
