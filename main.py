from __future__ import annotations


from hanual.lang.preprocess.preprocesser import PrePeoccesser
from hanual.optim.optimizer_handeler import OptimizerHandeler
from hanual.compile.compile_manager import CompileManager
from hanual.lang.builtin_parser import get_parser
from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.util.dump_tree import dump_tree
from hanual.lang.nodes.block import CodeBlock
from hanual.serialize import DumpFile
from pprint import PrettyPrinter
from hashlib import sha256


pp = PrettyPrinter()


class HanualMainClass:
    def __init__(self) -> None:
        self.preproc = PrePeoccesser()
        self.parser = get_parser()
        self.lexer = HanualLexer()

        # self.parser.toggle_debug_messages(True)

    def run(self, src: str) -> CodeBlock:
        whisper = self.preproc.process(src, starting_defs=["__testing_lang__"])
        whisper = self.lexer.tokenize(whisper)
        whisper = self.parser.parse(whisper)  # [0][1]
        return whisper


main = HanualMainClass()


src = r"""
fn main() {
    print("Hello world")
}
"""

res = main.run(src)

print(dump_tree(res, depth=12))


cm = CompileManager(res[0][1])

cm.collect_constants()
cm.collect_names()
cm.compile_tree()

print(dump_tree(cm))

op = OptimizerHandeler()

code = op.proof_read(cm)
print(dump_tree(code))

df = DumpFile()

df.dump_head(0, 0, 0, sha256(src.encode("utf-8")), append=True)
df.dump_deps(["toy.fr"], append=True)
df.dump_func_head({"main": 0}, append=True)
df.dump_constants(code.consts, append=True)
df.dump_instructions(cm, append=True)

with open("bin/hworld.chnl", "wb") as f:
    f.write(df.bytes)
