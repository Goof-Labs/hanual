# This class is a wrapper around all the code in the lang directory
from __future__ import annotations

from .preprocess.preprocesser import PrePeoccesser
from .builtin_parser import get_parser, PParser
from typing import Optional, TYPE_CHECKING
from .builtin_lexer import HanualLexer


if TYPE_CHECKING:
    from hanual.cli.__main__ import CompilerSettings


class BuiltinWrapper:
    # This class wiss spit out the ast

    __slots__ = "_preproc", "_lexer", "_parser", "_assembler"

    def __init__(
        self,
        preprocesser: Optional[PrePeoccesser] = None,
        lexer: Optional[HanualLexer] = None,
        parser: Optional[PParser] = None,
        asembler: Optional[Assembler] = None,
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

        # assembeler

        if asembler is None:
            self._assembler = Assembler()

        else:
            assert isinstance(asembler, Assembler)
            self._assembler = asembler

    def parse(self, src: str, flags: CompilerSettings):
        # TODO prefix
        whisper = self._preproc.process(
            src, prefix="@", starting_defs=flags.definitions
        )
        whisper = self._lexer.tokenize(whisper)

        self._parser.toggle_debug_messages(True)

        whisper = self._parser.parse(whisper)
        return whisper
