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

    def run(self, src: str) -> CodeBlock:
        whisper = self.preproc.process(src, starting_defs=["__testing_lang__"])
        whisper = self.lexer.tokenize(whisper)
        whisper = self.parser.parse(whisper)
        whisper = self.clean(whisper)
        # whisper = self.compiler.compile(whisper)
        # whisper = self.dump.dump(whisper, src)
        return whisper

    def clean(self, res_):
        res = CodeBlock(res_)
        return res


main = HanualMainClass()

res = main.run(
    r"""
[x] do
    x + 1
end
"""
)
pp.pprint(res)
pp.pprint(res.as_dict())
