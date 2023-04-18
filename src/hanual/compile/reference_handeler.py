class ReferenceHandeler:
    def __init__(self, cls) -> None:
        self._cls = cls

    def add_ref(self, name):
        self._cls._refs.append(name)
        return len(self._cls._refs)
