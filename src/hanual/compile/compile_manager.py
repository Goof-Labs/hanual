from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hanual.lang.nodes.base_node import BaseNode


class CompileManager:
    def __init__(self, tree) -> None:
        self._tree: BaseNode = tree
        self._instructions = []
        self._names = []
        self._const = []

    def compile_priority(self):
        """
        CompilePriority is for nodes such as functions. This is because
        functions should be compiled at the start of the file and not
        the middle. The example shows how the tree wold be genorated
        without this.

        Instructions
        Instructions
        Instructions

        FUNCTION_1_ENTERY

        Function_instructions
        Function_instructions
        Function_instructions

        RET

        Instructions
        Instructions
        Instructions

        This is a clear problem, so instead of compiling functions in place
        we make a function [this function] that wil get all functions
        definitions and then compile then. Then everything else can be
        compiled.
        """

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
