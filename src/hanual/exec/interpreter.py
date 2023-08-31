from __future__ import annotations

from hanual.lang.nodes import CodeBlock, Arguments
from .result import Result
from .scope import Scope


class HLPrint:
    @property
    def arguments(self):
        rgs = Arguments(["x"])
        rgs.function_def = True
        return rgs

    def __call__(self, scope):
        print(scope.get("x"))
        return Result().success(None)


class Interpreter:
    def __init__(self, tree: CodeBlock):
        self._tree: CodeBlock = tree

    def run(self):
        with Scope(parent=None, name="global") as scope:
            self._tree.execute(scope=scope)

            scope.set("println", HLPrint())

            scope.get("main", None)(scope=scope)
