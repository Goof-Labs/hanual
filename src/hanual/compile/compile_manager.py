from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional
from dataclasses import dataclass

if TYPE_CHECKING:
    from hanual.lang.nodes.base_node import BaseNode
    from hanual.compile.constants import Constant
    from hanual.compile.label import Label


@dataclass
class ItemData:
    consts: Optional[List[Constant]]
    names: Optional[List[str]]


class CompileManager:
    __slots__ = "_tree", "_instructions", "_items", "_file_deps", "_fn_table",

    def __init__(self, tree) -> None:
        self._items = ItemData(None, None)
        self._tree: BaseNode = tree
        self._instructions = []
        self._file_deps = []
        self._fn_table = {}

    def collect_items(self):
        self.collect_constants()
        self.collect_names()
        self.compile_tree()

    def collect_names(self):
        if self._items.names:
            return

        self._items.names = list(set(self._tree.get_names()))

    def collect_constants(self):
        if self._items.consts:
            return

        self._items.consts = []
        consts = []

        for const in self._tree.get_constants():
            if const.value in consts:
                continue

            consts.append(const.value)
            self._items.consts.append(const)

    def compile_tree(self):
        if self._instructions:
            return

        self._instructions = self._tree.compile(cm=self)

    def add_function(self, name: str, jp: Label) -> None:
        self._fn_table[name] = jp

    def add_import(self, name: str) -> None:
        if name in self._file_deps:
            return

        self._file_deps.append(name)

    @property
    def instructions(self):
        return self._instructions

    @instructions.setter
    def instructions(self, val: List):
        self._instructions = val

    @property
    def fn_table(self):
        return self._fn_table

    @property
    def names(self):
        return self._items.names

    @property
    def consts(self):
        return self._items.consts

    @property
    def file_deps(self):
        return self._file_deps
