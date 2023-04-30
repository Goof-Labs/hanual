from __future__ import annotations


from typing import Generic, TypeVar, Dict, Any, Self
from multipledispatch import dispatch
from abc import ABC, abstractmethod


class InterfaceConstPoolAdd(ABC):
    @abstractmethod
    def add_consts(self, consts: Dict[str, Any]) -> None:
        raise NotImplementedError


CLS = TypeVar("CLS", bound=InterfaceConstPoolAdd)
VALUE = TypeVar("VALUE")


class ConstPoolMod(Generic[CLS, VALUE]):
    """
    This class is used to add constants to a HanualFileFormat, this is sort of a proxy class, this just prevented me
    from having to implement all these methods directly on the main class, I can also use this class for an external
    python api.

    The dispatch decorator is used to allow one function to take in any parameter type and call a specific function
    this is like overloading in other strongly typed languages.
    """

    def __init__(self, instance: CLS) -> None:
        self._const_pool: Dict[str, VALUE] = {}
        self._instance = instance

    @dispatch(None, dict)
    def add_const(self, consts: Dict[str, VALUE]) -> Self:
        for name, value in consts.items():
            assert isinstance(name, str) is True

            self._const_pool[name] = value

        return self

    @dispatch(None, str, None)
    def add_const(self, name: str, value: VALUE) -> Self:
        self._const_pool[name] = value
        return self

    @dispatch(None, list)
    def add_const(self, consts: list[str, VALUE]) -> Self:
        for name, value in consts:
            assert isinstance(name, str)

            self._const_pool[name] = value

        return self

    @dispatch(None, tuple)
    def add_const(self, consts: tuple[str, VALUE]) -> Self:
        for name, value in consts:
            assert isinstance(name, str)

            self._const_pool[name] = value

        return self

    def get_instances(self) -> Dict[str, VALUE]:
        return self._const_pool

    def remove(self, name: str) -> Self:
        if name in self._const_pool.keys():
            del self._const_pool[name]

        return self

    def finalize(self):
        self._instance.add_consts(self._const_pool)
