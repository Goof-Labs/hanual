from __future__ import annotations

from hanual.lang.preprocess.preprocesser import Preprocessor
from hanual.compile.back_end.compiler import Compiler
from hanual.lang.util.line_range import LineRange
from hanual.lang.builtin_parser import get_parser
from hanual.lang.builtin_lexer import HanualLexer


def compile_code(code) -> tuple[any, str, LineRange]:
    pp = Preprocessor()
    lines = pp.process(code)

    lexer = HanualLexer()
    tokens = lexer.tokenize(lines, mode="compile")

    parser = get_parser()
    frame = parser.parse(tokens)[0]

    Compiler.from_ast(frame.value)
    return
