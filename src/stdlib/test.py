from hanual.compile.serialization.dump import HanualFileSerializer
from hanual.lang.preprocess.preprocesser import PrePeoccesser
from hanual.lang.builtin_parser import get_parser
from hanual.lang.builtin_lexer import HanualLexer
from hanual.compile.compile import Compiler
from pprint import PrettyPrinter
from sys import argv


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
        whisper = self.compiler.compile(whisper[0])
        whisper = self.dump.dump(whisper, src)
        return whisper


main = HanualMainClass()

fp = argv[1]

with open(f"{fp}.hnl", "r") as f:
    code = main.run(f.read())

with open(rf"obj\{fp}.chl", "wb") as f:
    f.write(code)
