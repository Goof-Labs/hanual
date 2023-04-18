from .global_state import GlobalState


class Compiler:
    def __init__(self) -> None:
        self._global_state = GlobalState()

    def compile(self, tree):
        print(tree)
        return tree.compile(self._global_state)
