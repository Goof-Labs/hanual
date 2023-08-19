from __future__ import annotations


from hanual.lang.preprocess.preprocesser import PrePeoccesser
from hanual.optim.optimizer_handeler import OptimizerHandeler
from hanual.compile.compile_manager import CompileManager
from hanual.lang.builtin_parser import get_parser
from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.util.dump_tree import dump_tree
from hanual.checkers.ast import verifiy
from hanual.serialize import DumpFile
from pprint import PrettyPrinter
from hashlib import sha256


pp = PrettyPrinter()


preproc = PrePeoccesser()
parser = get_parser()
lexer = HanualLexer()


src = r"""
fn main() {
    if i < 10 {}
    elif i > 10 {}
}
"""
whisper = preproc.process(src, starting_defs=["__testing_lang__"])
whisper = lexer.tokenize(whisper)
whisper = parser.parse(whisper)
res = verifiy(whisper)


print(dump_tree(res, depth=12))


cm = CompileManager(res[0][1])

cm.collect_constants()
cm.collect_names()
cm.compile_tree()


op = OptimizerHandeler()

code = op.proof_read(cm)
print(dump_tree(code))

df = DumpFile()

df.dump_head(0, 0, 0, sha256(src.encode("utf-8")), append=True)
df.dump_deps(["awsome.de"], append=True)
df.dump_func_head({"main": 0}, append=True)
df.dump_constants(code.consts, append=True)
df.dump_instructions(cm, append=True)

with open("bin/hworld.chnl", "wb") as f:
    f.write(df.bytes)
