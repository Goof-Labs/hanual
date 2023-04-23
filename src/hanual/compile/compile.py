from .global_state import GlobalState


class Compiler:
    def __init__(self) -> None:
        self._global_state = GlobalState()

    def get_deps(self):
        return {
            "refs": self._global_state.refs,
            "consts": self._global_state.const_pool,
        }

    def compile_src(self, tree):
        print(tree)
        return tree.compile(self._global_state)

    def compile(self, tree):
        return self.get_deps(), self.compile_src(tree)
