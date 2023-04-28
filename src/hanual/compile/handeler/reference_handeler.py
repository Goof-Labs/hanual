class ReferenceHandeler:
    def __init__(self, cls) -> None:
        self._cls = cls

    def add_ref(self, name: str):
        self._cls.refs.append(name)
        return len(self._cls.refs)-1
