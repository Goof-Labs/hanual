from typing import Callable


class ExportableModule:
    def __init__(self, **kwargs: Callable) -> None:
        for name, func in kwargs.items():
            ...
