from __future__ import annotations


from .lexer import Lexer, rx, kw, Token


class HanualLexer(Lexer):
    rules = [
        # NAMES
        ("CTX", rx(r"\$[a-zA-Z_][a-zA-Z0-9_]*")),
        ("MNM", rx(r"\~[a-zA-Z_][a-zA-Z0-9_]*")),
        ("ADT", rx(r"\\[a-zA-Z0-9_]+")),  # algebraic datatype \name
        ("ID", rx(r"[a-zA-Z_][a-zA-Z0-9_]*")),
        # KEYWORDS
        ("FN", kw("fn")),
        ("AS", kw("as")),
        ("IF", kw("if")),
        ("DO", kw("do")),
        ("FOR", kw("for")),
        ("LET", kw("let")),
        ("END", kw("end")),
        ("NEW", kw("new")),
        ("USE", kw("use")),
        ("ITR", kw("iter")),
        ("EIF", kw("elif")),
        ("ELS", kw("else")),
        ("ELS", kw("else")),
        ("WHL", kw("while")),
        ("LOOP", kw("loop")),
        ("WHR", kw("where")),
        ("RET", kw("return")),
        ("SCT", kw("struct")),
        ("SHOUT", kw("SHOUT")),
        ("BREAK", kw("break")),
        ("FREEZE", kw("freeze")),
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
        ("COL", rx(r"\:")),
        ("DOT", rx(r"\.")),
        ("LSB", rx(r"\[")),
        ("RSB", rx(r"\]")),
        # special cases
        ("NEWLINE", rx(r"\n")),
        ("SKIP", rx(r"[ \t]+|//.*|/\*[^*]*\*+(?:[^/*][^*]*\*+)*/")),
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
