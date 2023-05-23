from __future__ import annotations

from hanual.compile.serialization.dump import HanualFileSerializer
from hanual.lang.preprocess.preprocesser import PrePeoccesser
from hanual.lang.builtin_parser import get_parser
from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.util.dump_tree import dump_tree
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

        self.parser.toggle_debug_messages(True)

    def run(self, src: str) -> CodeBlock:
        whisper = self.preproc.process(src, starting_defs=["__testing_lang__"])
        whisper = self.lexer.tokenize(whisper)
        whisper = self.parser.parse(whisper)[0][1]
        whisper = self.compiler.compile(whisper)
        # whisper = self.dump.dump(whisper, src)
        return whisper


main = HanualMainClass()

with open(r"D:\programing\hanual\hanual\src\stdlib\io.hnl") as f:
    res = main.run(f.read())

r"""
use std::bufferlib::string_builder as str_builder
use std::bufferlib::add_char
use std::foundation::printc
use std::foundation::getch
use std::strlib::str_len
use std::strlib::getc


fn print(value)
    let i = 0

    while ( i < str_len(value))
        printc(getc(value, i))
        i = i + 1
    end
end

print("Hello world")

"""
print(main.compiler.assembler.get_asm())
# pp.pprint(res.instructions)
# pp.pprint(res.deps)
# pp.pprint(res)

# print(dump_tree(res, depth=25))
# pp.pprint(res.as_dict())
