from __future__ import annotations

from doc_parser import parse_doc_string
from typing import Callable
import inspect


class FunctionDocumentation:
    __slots__ = "_name", "_params", "_doc", "_param_doc"

    def __init__(self, function: Callable) -> None:
        self._name = function.__name__
        self._params = inspect.getfullargspec(function)
        self._doc = parse_doc_string(function.__doc__)

        self._param_doc = {}

        for (p_name, p_type, summary, doc) in self._doc["params"]:
            if p_name not in self._params.args:
                raise Warning

            self._param_doc[p_name] = (p_type, summary, doc)

    @property
    def name(self) -> str:
        return self._name

    @property
    def params(self):
        return self._param_doc
