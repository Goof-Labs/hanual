from typing import NamedTuple
import re


def kw(reg):
    return reg, "kw"


def rx(reg):
    return reg, "rx"


class Token(NamedTuple):
    type: str
    value: str
    line: int
    colm: int


class Lexer:
    def __init__(self):
        self._rules = []
        self._kwrds = []

        for rule in self.rules:
            if rule[1][1] == "kw":
                self._kwrds.append(rule[0])

            else:
                self._rules.append((rule[0], rule[1][0]))

    def tokenize(self, stream: str) -> None:
        tok_reg = "|".join("(?P<%s>%s)" % pair for pair in self._rules)

        line_no = 1
        line_start = 0

        for pat in re.finditer(tok_reg, stream):
            kind = pat.lastgroup
            valu = pat.group()
            col = pat.start() - line_start

            if valu in self._kwrds:
                kind = valu

            elif kind == "NEWLINE":
                line_start = pat.end()
                line_no += 1
                continue

            elif kind == "SKIP":
                continue

            elif kind == "MISMATCH":
                raise RuntimeError(f"{valu!r} was unexpected on line {line_no}")

            if hasattr(self, f"t_{kind}"):
                yield getattr(self, f"t_{kind}")(kind, valu, line_no, col)
                continue

            yield Token(kind, valu, line_no, col)


class MyLex(Lexer):
    rules = (
        ("ID", rx(r"[a-zA-Z_][a-zA-Z0-9_]*")),
        ("SHOUT", kw("SHOUT")),
        ("OP", rx(r"[\+\-\\\*]")),
        ("NUM", rx(r"\d+(\.\d*)?")),
        # special cases
        ("NEWLINE", rx(r"\n")),
        ("SKIP", rx(r"[ \t]+")),
        ("MISMATCH", rx(r".")),
    )

    def t_NUM(self, kind: str, valu: str, line_no: int, col: int) -> Token:
        return Token(kind, float(valu) if "." in valu else int(valu), line_no, col)

