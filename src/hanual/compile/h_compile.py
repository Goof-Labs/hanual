from __future__ import annotations

from hanual.compile.optim.optimizer_handeler import OptimizerHandler
from hanual.compile.compile_manager import CompileManager
from hanual.tools.cli import HanualCli, CompilerOptions
from hanual.compile.serialize.dump_file import DumpFile
from hanual.lang.builtin_parser import get_parser
from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.preprocess import Preprocessor
from hanual.api.load_hooks import HookLoader
from typing import Optional, List, Mapping
from hanual.lang.pparser import PParser
from hanual.lang.nodes import CodeBlock
from hanual.lang.lexer import Lexer


def hl_compile(*,
               options: Optional[CompilerOptions] = None,
               preproc: Optional[Preprocessor] = None,
               hook_loader: Optional[HookLoader] = None,
               parser: Optional[PParser] = None,
               lexer: Optional[Lexer] = None,
               #  preproc arguments
               prefix: Optional[str] = None,
               starting_definitions: Optional[List[str]] = None,
               mappings: Optional[Mapping[str, str]] = None,
               ) -> None:
    # set default arguments and stuff
    if options is None:
        options = HanualCli().options

    if hook_loader is None:
        hook_loader = HookLoader()

    # setup hooks, we do need this before any other stuff is initialized
    if isinstance(options.inject, tuple):
        for module in options.inject:
            hook_loader.load_module(module, module.replace(".", "//") + ".py")

    elif isinstance(options.inject, str):
        hook_loader.load_module(options.inject, options.inject.replace(".", "//") + ".py")

    else:
        raise Exception

    # Default arguments and stuff
    if preproc is None:
        preproc = Preprocessor(
            prefix=prefix,
            pre_defs=starting_definitions,
            hooks=hook_loader.preproc,
        )

        for hook in hook_loader.preproc:
            preproc.add_hook(hook)

    if parser is None:
        parser = get_parser()
        parser.add_hooks(hook_loader.rules)

    if lexer is None:
        lexer = HanualLexer()
        lexer.add_hooks(hook_loader.tokens)

    # preprocessing

    if not options.files:
        raise Exception("No files specified")

    file = options.files[0] if isinstance(options.files, tuple) else options.files

    with open(file, "r") as f:
        text = preproc.process(text=f.read(),
                               prefix=prefix,
                               starting_defs=starting_definitions,
                               mappings=mappings)

    # tokenizing/lexing

    lexer.add_hooks(hook_loader.tokens)

    tokens = lexer.tokenize(text)

    # parsing

    parser.add_hooks(hook_loader.rules)

    tree: CodeBlock = parser.parse(tokens)[0][1]

    # compile the ast

    cm = CompileManager(tree)
    cm.collect_items()
    cm.compile_tree()

    # optimizations
    op = OptimizerHandler()
    code = op.proof_read(cm.instructions)

    df = DumpFile()
    df.dump_file(cm, code, (0, 0, 0), text)
