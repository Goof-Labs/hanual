from __future__ import annotations


from hanual.compile.instruction import Instruction
from typing import NamedTuple, List
from hanual.lang.lexer import Token
from .assembler import Assembler


class DepInfo(NamedTuple):
    file_deps: List[str]
    consts: List[Token]


class CompileInfo(NamedTuple):
    instructions: List[Instruction]
    deps: DepInfo


class Compiler:
    def __init__(self) -> None:
        self._assembler = Assembler()

    def get_deps(self):
        return DepInfo(
            file_deps=self._assembler._external_fls,
            consts=self._assembler._external_fns,
        )

    def compile_src(self, tree):
        tree.compile(self._assembler)
        return self._assembler._code

    @property
    def assembler(self):
        return self._assembler

    def compile(self, tree):
        return CompileInfo(
            instructions=self.compile_src(tree),
            deps=self.get_deps(),
        )
