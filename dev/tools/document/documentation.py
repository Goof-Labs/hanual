from __future__ import annotations

from doc_parser import parse_doc_string
from typing import Self, Callable
import inspect


class FunctionDocumentation:
    __slots__ = "",

    def __init__(self, function: Callable) -> None:
        self._name = function.__name__
        self._params = inspect.getfullargspec(function)
        self._doc = parse_doc_string(function.__doc__)

        self._param_doc = {}

        for (p_name, p_type, summary, doc) in self._doc["params"]:
            if not p_name in self._params.args:
                raise Warning


class ClassDocumentation:
    def __init__(self) -> None:
        pass

class DocumentationGenerator:
    def __init__(self) -> None:
        ...
