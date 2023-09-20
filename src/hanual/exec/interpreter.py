from __future__ import annotations

from .hl_builtin.func_builtin import FuncBuiltinLibrary
from .hl_builtin.io_builtin import IOBuiltinLibrary
from hanual.lang.nodes import CodeBlock
from .scope import Scope


class Interpreter:
    def __init__(self, tree: CodeBlock):
        self._tree: CodeBlock = tree

    def run(self):
        with Scope(parent=None, name="global") as scope:
            self._tree.execute(scope=scope)

            for func in (*IOBuiltinLibrary().get_builtins(), *FuncBuiltinLibrary().get_builtins()):
                scope.set(func.name, func)

            _, err = scope.get("main", None)(scope=scope)

            if err:
                print(err.as_string())
