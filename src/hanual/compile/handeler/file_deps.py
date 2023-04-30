from __future__ import annotations


class ExternDepsHandeler:
    def __init__(self, cls) -> None:
        self.cls = cls

    def add_dependency(self, file_name):
        self.cls.add_dep(file_name)

    def get_dependency(self):
        return self.cls._file_deps
