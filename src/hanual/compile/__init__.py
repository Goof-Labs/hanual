from __future__ import annotations

from hanual.lang.preprocess.preprocesser import PrePeoccesser
from typing import Union, List, Literal, Self
from hanual.lang.builtin_lexer import Lexer
from hanual.lang.pparser import PParser
from hanual.lang import builtin_parser
from .varpool import VarPool
from .labels import Labels


class _CompilerFlags:
    mode: Union[Literal["relese"], Literal["debug"], Literal["run"]] = "run"
    starting_definitions: List[str] = []
    # the stage we would stop compilation, e.g after preprocessers
    stop_at: Union[int, None] = None
    preproc_prefix: str = "@"


class GlobalState:
    __slots__ = ("_vars", "_labels")

    __instance = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = type(cls).__init__()

        return cls.__instance

    def __init__(self) -> None:
        self._vars = VarPool()
        self._idx = 0

    @property
    def vars(self) -> VarPool:
        return self._vars

    @property
    def labels(self) -> Labels:
        return self._labels

    @property
    def position(self):
        return self._idx

    def advance(self):
        self._idx += 1


class Compiler:
    def __init__(self, flags: _CompilerFlags) -> None:
        self._flags = flags

        self.parser: PParser = builtin_parser.get_parser()  # actually a modual
        self.preprocesser: PrePeoccesser = PrePeoccesser()
        self.lexer: Lexer = Lexer()

        self.preprocesser.prefix = self._flags.preproc_prefix

    @property
    def flags(self) -> _CompilerFlags:
        return self._flags

    def compile(self: Compiler, src: str):
        self.preprocesser.add_definition(self._flags.mode.upper())

        # a bad reference to `chineese whispers` where a message gets passed to one stage of compilation and then moddified
        whisper = src

        if self._flags.stop_at >= 1:
            # preproc
            whisper: str = self.preprocesser.process(whisper)

        if self._flags.stop_at >= 2:
            # lex
            whisper = self.lexer.tokenize(whisper)

        if self._flags.stop_at >= 3:
            # macros can F*CK the source code up badly so here is an extra step
            whisper = whisper  # TODO: ACTUALLY IMPLEMENT THIS

        if self._flags.stop_at >= 4:
            # parse
            whisper = self.parser.parse(whisper)

        if self._flags.stop_at >= 5:
            whisper = whisper()  # TODO: this as well

        return whisper
