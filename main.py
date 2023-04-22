from hanual.lang.preprocess.macro import make_parser, MacroLexer
from hanual.lang.preprocess.preprocesser import PrePeoccesser
from hanual.lang.preprocess.macro import SubstituteMacro
from hanual.lang.builtin_parser import get_parser
from hanual.lang.builtin_lexer import HanualLexer
from hanual.compile.compile import Compiler
from pprint import PrettyPrinter


pp = PrettyPrinter()


class HanualMainClass:
    def __init__(self) -> None:
        self.preproc = PrePeoccesser()
        self.compiler = Compiler()
        self.parser = get_parser()
        self.lexer = HanualLexer()

    def run(self, src: str) -> None:
        whisper = self.preproc.process(src)
        whisper = self.lexer.tokenize(whisper)
        whisper = self.parser.parse(whisper)
        whisper = self.compiler.compile(whisper[0])
        pp.pprint(whisper)


main = HanualMainClass()
main.run(
    """
use std::io

let x = 1

hello('Hello world')

fn test()
end
    """
)
