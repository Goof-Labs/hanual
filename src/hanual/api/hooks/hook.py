from __future__ import annotations


def props(**kwargs):
    def decor(cls):
        cls._props = kwargs
        return cls

    return decor


class GenericHook:
    __slots__ = "_props",

    @property
    def props(self):
        return self._props
