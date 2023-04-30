# This class is a wrapper around all the code in the lang directory
from __future__ import annotations


from .preprocess.preprocesser import PrePeoccesser
from hanual.cli.__main__ import CompilerSettings
from .builtin_parser import get_parser, PParser
from .builtin_lexer import HanualLexer
from typing import Optional


class BuiltinWrapper:

    # This class wiss spit out the ast

    __slots__ = "_preproc", "_lexer", "_parser"

    def __init__(
        self,
        preprocesser: Optional[PrePeoccesser] = None,
        lexer: Optional[HanualLexer] = None,
        parser: Optional[PParser] = None,
    ) -> None:

        # preproc setup
        if preprocesser is None:
            self._preproc = PrePeoccesser()

        else:
            assert isinstance(preprocesser, PrePeoccesser)
            self._preproc = preprocesser

        # lex setup
        if lexer is None:
            self._lexer = HanualLexer()

        else:
            assert isinstance(lexer, HanualLexer)
            self._lexer = lexer

        # parser setup
        if parser is None:
            self._parser = get_parser()

        else:
            assert isinstance(parser, PParser)
            self._parser = parser

    def parse(self, src: str, flags: CompilerSettings):
        ...
