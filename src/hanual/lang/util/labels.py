from __future__ import annotations


from typing import Generic, TypeVar, Dict, Any
from abc import ABC, abstractmethod


VALUE = TypeVar("VALUE", int, None)
NAME = TypeVar("NAME")


class LabelInterface(ABC):
    @abstractmethod
    def advance(self) -> None:
        raise NotImplementedError

    @abstractmethod
    @property
    def get_idx(self) -> VALUE:
        raise NotImplementedError


CLS = TypeVar("CLS", bound=LabelInterface)


class Label(Generic[CLS]):
    def __init__(self, cls: CLS) -> None:
        self._labels: Dict[NAME, VALUE] = {}

        self.cls: CLS = cls

    def get_label(self, name: NAME, default: Any = None) -> VALUE:
        if default:
            return self._labels.get(name, default)

        return self._labels[default]

    def put_label(self, name: NAME) -> None:
        self._labels[name] = self.cls.get_idx
        self.cls.advance()
