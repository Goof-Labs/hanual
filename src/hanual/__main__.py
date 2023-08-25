from __future__ import annotations

from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.builtin_parser import get_parser
from lang.preprocess import Preprocessor
from api.load_hooks import HookLoader
from tools.cli import HanualCli
import logging

logging.basicConfig(level=logging.DEBUG)

options = HanualCli().options
hl = HookLoader()

# INJECT CODE
if isinstance(options.inject, tuple):
    for module in options.inject:
        hl.load_module(module, module.replace(".", "//") + ".py")

elif isinstance(options.inject, str):
    hl.load_module(options.inject, options.inject.replace(".", "//") + ".py")

else:
    raise Exception

# preprocessing

preproc = Preprocessor(hooks=hl.preproc)

if not options.files:
    raise Exception("No files specified")

file = options.files[0] if isinstance(options.files, tuple) else options.files

with open(file, "r") as f:
    text = preproc.process(f.read())

# tokenizing/lexing

lexer = HanualLexer()

lexer.add_hooks(hl.tokens)

tokens = lexer.tokenize(text)

# parsing

parser = get_parser()

parser.add_hooks(hl.rules)
