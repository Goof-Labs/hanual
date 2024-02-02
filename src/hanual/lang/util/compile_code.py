from __future__ import annotations

from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.builtin_parser import get_parser
from hanual.lang.preprocess.preprocesser import Preprocessor
from hanual.lang.util.dump_tree import dump_tree
from hanual.wrappers.modle_wrapper import ModuleWrapper
from hanual.wrappers.function_wrapper import FunctionWrapper


def compile_code(code):
    pp = Preprocessor()
    lines = pp.process(code)

    lexer = HanualLexer()
    tokens = lexer.tokenize(lines, mode="compile")

    parser = get_parser()
    frames = parser.parse(tokens)

    mod = ModuleWrapper()

    for node in frames[0].value.children:
        mod.add(FunctionWrapper(node.gen_py_code()))
    
    print(mod)
