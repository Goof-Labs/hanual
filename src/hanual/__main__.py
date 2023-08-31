from __future__ import annotations

import logging

from hanual.lang.util.build_ast import create_ast
from hanual.compile.h_compile import hl_compile
from hanual.exec.interpreter import Interpreter
from hanual.tools.cli import HanualCli

logging.basicConfig(level=logging.DEBUG)

options = HanualCli().options

if "compile" in options.loose_args:
    hl_compile()

elif "pack" in options.loose_args:
    raise NotImplementedError

elif "run" in options.loose_args:
    ast, _ = create_ast()
    it = Interpreter(ast)
    it.run()

else:
    print(f"One of {options.loose_args!r} is not recognised as a mode")
