from __future__ import annotations

from .builtin_lexer import HanualLexer
from .builtin_parser import get_parser
from .preprocess.preprocesser import Preprocessor


def compile_code(code):
    pp = Preprocessor()
    lines = pp.process(code)

    lexer = HanualLexer()
    tokens = lexer.tokenize(lines, mode="compile")

    parser = get_parser()
    print(parser.parse(tokens))
