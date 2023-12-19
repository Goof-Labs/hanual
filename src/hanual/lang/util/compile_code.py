from __future__ import annotations

import dis

from hanual.compile.hanual_function import HanualFunction
from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.builtin_parser import get_parser
from hanual.lang.preprocess.preprocesser import Preprocessor

from hanual.lang.util.dump_tree import dump_tree


def compile_code(code):
    pp = Preprocessor()
    lines = pp.process(code)

    lexer = HanualLexer()
    tokens = lexer.tokenize(lines, mode="compile")

    parser = get_parser()
    frame = parser.parse(tokens)

    print(dump_tree(frame[0], depth=1000))

    func = HanualFunction.from_func(frame[0].value.children[0])
    out = func.compile()
    code = out.to_code()

    dis.dis(code)

    res = eval(code)
    print(res)

    return
