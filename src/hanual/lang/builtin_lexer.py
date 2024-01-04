from __future__ import annotations

from hanual.lang.data import LiteralWrapper
from hanual.lang.util.line_range import LineRange

from .lexer import Lexer, Token, kw, rx


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
        # ("END", kw("end")),
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
        ("OP", rx(r"[\+\-\/\*]")),
        ("NUM", rx(r"\d+(\.\d+)?")),
        ("COM", rx(r"\,")),
        ("NSA", rx(r"\:\:")),  # name space access
        ("COL", rx(r"\:")),
        ("DOT", rx(r"\.")),
        ("LSB", rx(r"\[")),
        ("RSB", rx(r"\]")),
        ("LCB", rx(r"\{")),
        ("RCB", rx(r"\}")),
        ("BAR", rx(r"\|")),
    ]

    last = [
        # special cases
        ("SKIP", rx(r"[ \t]+|//.*|/\*[^*]*\*+(?:[^/*][^*]*\*+)*/")),
        ("MISMATCH", rx(r".")),
    ]

    @staticmethod
    def t_compile_NUM(
            kind: str, value: str, line_num: int, col: int, origin_line: str
    ) -> Token:
        return Token(
            token_type=kind,
            value=float(value) if "." in value else int(value),
            line_range=LineRange(line_num, line_num),
            colm=col,
            lines=origin_line,
        )

    @staticmethod
    def t_exec_NUM(
            kind: str, value: str, line_num: int, col: int, origin_line: str
    ) -> Token:
        return Token(
            kind,
            LiteralWrapper(float(value)),
            LineRange(line_num, line_num),
            col,
            origin_line,
        )

    @staticmethod
    def t_exec_STR(
            kind: str, value: str, line_num: int, col: int, origin_line: str
    ) -> Token:
        # remove the last and first character of string, which are " or double quotes
        value = value[1:]
        value = value[:-1]
        return Token(
            kind,
            LiteralWrapper(value),
            LineRange(line_num, line_num),
            col,
            origin_line,
        )

    @staticmethod
    def t_compile_STR(
            kind: str, value: str, line_num: int, col: int, origin_line: str
    ) -> Token:
        # remove the last and first character of string, which are " or double quotes
        value = value[1:]
        value = value[:-1]
        return Token(
            kind,
            value,
            LineRange(line_num, line_num),
            col,
            origin_line,
        )
