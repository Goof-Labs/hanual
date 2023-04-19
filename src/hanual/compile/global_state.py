from .reference_handeler import ReferenceHandeler
from .const_handeler import ConstantHandeler
from .labels import LabelHandeler


class GlobalState:
    __instance = None

    def __init__(self) -> None:
        self.__instance = self

        self._const_pool = []
        self._label_pool = []
        self._functions = []
        self._refs = []

    @property
    def refs(self):
        return self._refs

    @property
    def const_pool(self):
        return self._const_pool

    @property
    def get_instacne(self):
        return self.__instance

    @property
    def labels(self):
        return LabelHandeler(self)

    @property
    def constants(self):
        return ConstantHandeler(self)

    @property
    def references(self):
        return ReferenceHandeler(self)

    def add_function(self, name: str):
        self._functions.append(name)
