from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hanual.lang.nodes.base_node import BaseNode


class CompileManager:
    def __init__(self, tree) -> None:
        self._tree: BaseNode = tree
        self._instructions = []
        self._names = []
        self._const = []

    def collect_names(self):
        self._names = self._tree.get_names()

    def collect_constants(self):
        self._const = []
        consts = []

        for const in self._tree.get_constants():
            if const.value in consts:
                continue

            consts.append(const.value)
            self._const.append(const)

    def compile_tree(self):
        self._instructions = self._tree.compile()

    @property
    def instructions(self):
        return self._instructions

    @property
    def names(self):
        return self._names

    @property
    def consts(self):
        return self._const
