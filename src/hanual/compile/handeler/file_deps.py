class ExternDepsHandeler:
    def __init__(self, cls) -> None:
        self.cls = cls

    def add_dependancy(self, file_name):
        self.cls.add_dep(file_name)
