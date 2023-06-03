from __future__ import annotations


from hanual.lang.errors import Error, HNLFileNotFound
from hanual.runtime.status import ExecStatus
from typing import TYPE_CHECKING, Any, Union
from .base_node import BaseNode
from os import environ
from abc import ABC
import pathlib

if TYPE_CHECKING:
    from hanual.runtime.runtime import RuntimeEnvironment
    from .namespace_acessor import NamespaceAccessor


class UsingStatement(BaseNode, ABC):
    __slots__ = ("_nsa",)

    def __init__(self: BaseNode, nsa: NamespaceAccessor) -> None:
        self._loaded_path = None
        self._nsa = nsa

    @property
    def path(self):
        return self._nsa

    @property
    def loaded_path(self) -> Union[None, pathlib.Path]:
        return self._loaded_path

    def compile(self, ir) -> None:
        raise NotImplementedError

    def execute(self, rte: RuntimeEnvironment) -> ExecStatus[Error, Any]:
        for path in environ["path"].split(";"):
            if pth := pathlib.Path(path + self._nsa.full_path + ".hnl").is_file():
                rte.add_search_path(pth)
                self._loaded_path = pth

                return ExecStatus(None, self)

        return ExecStatus(HNLFileNotFound(), self)

    def as_dict(self):
        super().as_dict()
