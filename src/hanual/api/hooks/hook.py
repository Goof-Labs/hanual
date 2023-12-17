from __future__ import annotations


def props(**kwargs):
    """Used to define properties on a GenericHook

    > A class decorator that is used to define properties
    > on a class.
    > Example
    >
    > @props(some_prop="some_value")

    @kwargs^dict[str, any]>properties to define
    | Takes any keywprd argument and attaches them to a
    | Hook, this hook must inherit from `GenericHook`.
    """

    def decor(cls):
        cls._props = kwargs
        return cls

    return decor


class GenericHook:
    """Base class for all hooks.

    > All Hooks need to inherit from this cass which are implemented
    > internally. If you are just creating a hook that, for example,
    > adds a new preprocessor, then you do not need to inherit from
    > this class.
    """

    __slots__ = ("_props",)

    @property
    def props(self):
        """Used to get the properties defined by `@props`"""
        return self._props
