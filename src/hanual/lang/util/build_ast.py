from __future__ import annotations

from sys import argv
from typing import Generator, List, Literal, Mapping, Optional, Tuple, Union

from hanual.api.load_hooks import HookLoader
from hanual.lang.builtin_lexer import HanualLexer
from hanual.lang.builtin_parser import get_parser
from hanual.lang.errors import ErrorType, HanualError, TraceBack
from hanual.lang.lexer import Lexer
from hanual.lang.nodes import CodeBlock
from hanual.lang.pparser import PParser
from hanual.lang.preprocess import Preprocessor
from hanual.lang.util.dump_tree import dump_tree
from hanual.tools.cli import CompilerOptions, HanualCli


def create_ast(
    *,
    options: Optional[CompilerOptions] = None,
    preproc: Optional[Preprocessor] = None,
    hook_loader: Optional[HookLoader] = None,
    parser: Optional[PParser] = None,
    lexer: Optional[Lexer] = None,
    #  preproc arguments
    prefix: Optional[str] = None,
    starting_definitions: Optional[List[str]] = None,
    mappings: Optional[Mapping[str, str]] = None,
    #  Lexer arguments
    lexer_mode: Union[Literal["exec"], Literal["compile"], None] = None,
) -> Tuple[CodeBlock, Generator[str, None, None]]:
    # set default arguments and stuff
    if options is None:
        options = HanualCli().parse_config().options

    if hook_loader is None:
        hook_loader = HookLoader()

    # setup hooks, we do need this before any other stuff is initialized
    if isinstance(options.inject, tuple):
        for module in options.inject:
            hook_loader.load_module(module, module.replace(".", "//") + ".py")

    elif isinstance(options.inject, str):
        hook_loader.load_module(
            options.inject, options.inject.replace(".", "//") + ".py"
        )

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

    # check optional arguments
    if lexer_mode is None:
        if "compile" in options.loose_args:
            lexer_mode = "compile"

        elif "run" in options.loose_args:
            lexer_mode = "exec"

        else:
            raise Exception("couldn't infer lexer mode, try passing it as an argument")

    # preprocessing

    if not options.files:
        print(
            HanualError(
                pos=("SHELL", 0, 0),
                line=" ".join(argv) + "\n",
                name=ErrorType.cli_argument_unresolved,
                tip="Try passing the argument like this: files=my_file.hnl",
                reason="The `files` argument was not passed as a paramiter",
                tb=TraceBack(),
            ).as_string()
        )
        exit(1)

    with open(options.files[0], "r") as f:
        text = preproc.process(
            text=f.read(),
            prefix=prefix,
            starting_defs=starting_definitions,
            mappings=mappings,
        )

    # tokenizing/lexing

    lexer.add_hooks(hook_loader.tokens)

    tokens = lexer.tokenize(text, mode=lexer_mode)

    # parsing

    parser.add_hooks(hook_loader.rules)

    tree = parser.parse(tokens)  # [0][1]
    return tree[0][1], text
