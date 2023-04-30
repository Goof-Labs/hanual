from __future__ import annotations


from .assembler import Assembler


class Compiler:
    def __init__(self) -> None:
        self._assembler = Assembler()

    def get_deps(self):
        return {
            "deps": self._assembler.file_deps,
            "refs": self._assembler.refs,
            "consts": self._assembler.constants,
        }

    def compile_src(self, tree):
        tree.compile(self._assembler)
        return self._assembler.instructions

    def compile(self, tree):
        return self.compile_src(tree), self.get_deps()

    def dump_file(self, tree):
        return self.get_deps()
