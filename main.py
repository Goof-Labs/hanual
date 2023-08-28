from __future__ import annotations

import time
from hashlib import sha256
from pprint import PrettyPrinter

from hanual.compile.compile_manager import CompileManager
from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.builtin_parser import get_parser
from hanual.lang.preprocess.preprocesser import Preprocessor
from hanual.lang.util.dump_tree import dump_tree
from hanual.compile.optim.optimizer_handeler import OptimizerHandler
from hanual.compile.serialize import DumpFile

start = time.perf_counter()

pp = PrettyPrinter()


preproc = Preprocessor()
parser = get_parser()
lexer = HanualLexer()


src = r"""
fn main() {
    println("Hello world")
}
"""
whisper = preproc.process(open("test/test.hnl").read(), starting_defs=["__testing_lang__"])
whisper = lexer.tokenize(whisper)
whisper = parser.parse(whisper)


# print(dump_tree(res, depth=12))


cm = CompileManager(whisper[0][1])

cm.collect_constants()
cm.collect_names()
cm.compile_tree()


op = OptimizerHandler()

code = op.proof_read(cm)
# print(dump_tree(code))

df = DumpFile()

df.dump_head(0, 0, 0, sha256(src.encode("utf-8")), append=True)
df.dump_deps(["awsome.de"], append=True)
df.dump_func_head({"main": 0}, append=True)
df.dump_constants(code.consts, append=True)
df.dump_instructions(cm, append=True)

# with open("bin/hworld.chnl", "wb") as f:
#    f.write(df.bytes)

end = time.perf_counter()

print(end - start)

print(dump_tree(cm))
