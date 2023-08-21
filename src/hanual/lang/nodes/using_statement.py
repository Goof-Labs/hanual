from __future__ import annotations

import pathlib
from abc import ABC
from os import environ
from typing import TYPE_CHECKING, Union

from hanual.compile.constant import Constant

from .base_node import BaseNode

if TYPE_CHECKING:
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

    def get_constants(self) -> list[Constant]:
        return []

    def get_names(self) -> list[str]:
        return []

    def execute(self):
        ...
