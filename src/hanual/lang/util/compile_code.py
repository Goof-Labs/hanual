from __future__ import annotations

from hanual.lang.preprocess.preprocesser import Preprocessor
from hanual.lang.builtin_parser import get_parser
from hanual.lang.builtin_lexer import HanualLexer
from hanual.compile.hanual_function import HanualFunction


def compile_code(code):
    pp = Preprocessor()
    lines = pp.process(code)

    lexer = HanualLexer()
    tokens = lexer.tokenize(lines, mode="compile")

    parser = get_parser()
    frame = parser.parse(tokens)

    func = HanualFunction.from_func(frame[0].value.children[0])
    func.compile()
    return func
