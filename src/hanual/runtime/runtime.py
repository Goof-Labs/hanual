class RuntimeEnvironment:
    def __init__(self) -> None:
        self._search_paths = []

    def add_search_path(self, path):
        self._search_paths.append(path)
