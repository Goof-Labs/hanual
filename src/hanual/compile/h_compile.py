from __future__ import annotations

from hanual.compile.optim.optimizer_handeler import OptimizerHandler
from hanual.compile.compile_manager import CompileManager
from hanual.compile.serialize.dump_file import DumpFile
from hanual.lang.util.build_ast import create_ast


def hl_compile(**kwargs) -> None:
    tree, text = create_ast(**kwargs)
    # compile the ast

    cm = CompileManager(tree)
    cm.collect_items()
    cm.compile_tree()

    # optimizations
    op = OptimizerHandler()

    op.proof_read(cm)

    df = DumpFile()
    df.dump_file(cm, (0, 0, 0), text)
