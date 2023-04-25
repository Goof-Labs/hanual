from hanual.compile.serialization.dump import HanualFileSerializer
from hanual.lang.preprocess.preprocesser import PrePeoccesser
from hanual.lang.builtin_parser import get_parser
from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.nodes.block import CodeBlock
from hanual.compile.compile import Compiler
from pprint import PrettyPrinter

pp = PrettyPrinter()


class HanualMainClass:
    def __init__(self) -> None:
        self.dump = HanualFileSerializer()
        self.preproc = PrePeoccesser()
        self.compiler = Compiler()
        self.parser = get_parser()
        self.lexer = HanualLexer()

    def run(self, src: str) -> None:
        whisper = self.preproc.process(src)
        whisper = self.lexer.tokenize(whisper)
        whisper = self.parser.parse(whisper)
        whisper = self.clean(whisper)
        whisper = self.compiler.compile(whisper)
        pp.pprint(whisper)
        #pp.pprint(whisper[0])

    def clean(self, res):
        res = CodeBlock(res)
        return res


main = HanualMainClass()
main.run(
    """
print("hi")
    """
)
