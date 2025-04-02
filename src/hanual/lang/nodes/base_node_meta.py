from __future__ import annotations

from abc import ABCMeta
from typing import TYPE_CHECKING, Type

from hanual.lang.util.line_range import LineRange
from hanual.lang.util.node_utils import Intent
from hanual.util.equal_list import ItemEqualList
from hanual.util import ArgumentError

if TYPE_CHECKING:
    from hanual.lang.nodes.base_node import BaseNode


class _BaseNodeMeta(ABCMeta):
    """A class that validates the atributes of all sub-classes

    This class checks overrides the `__init__` and `gen_code` method. The
    `__init__` method now validates the input, the arguments that where given to
    it and sets the `_lines` and `_line_range`. The `gen_code` method converts
    the input arguments to an `ItemEqualList` and adds a try/except statement to
    better describe any stack traces.
    """
    def __new__(cls, *args, **kwargs) -> Type:
        instance = super().__new__(cls, *args, **kwargs)

        name, _, attrs = args

        instance.__init__ = cls.__override_init(instance, method=instance.__init__)
        instance.gen_code = cls.__overload_gen_code(instance, instance.gen_code)

        for attr_name, attr_value in attrs.items():
            if not isinstance(attr_value, Intent):
                continue

            attr_value.set_attrs(attr_name, 0)

        return instance

    def __override_init(cls, method):
        # This __init__ overrides the one in the class constructor; this is to inject a check to ensure that the
        # class can function correctly.
        # I am making this to help find bugs early when the class is defined, not when the code it is an object
        # floating around
        def __init__(self, *args, **kwargs):
            cls.__validate_input(method, args, kwargs)
            cls.__validate_method(self, method)

            self._lines = ""
            self._line_range = LineRange(start=float("inf"), end=float("-inf"))

            method(self, *args, **kwargs)

        return __init__

    def __overload_gen_code(cls, method):
        def decor(self, *args, **kwargs):
            try:
                yield from method(self, ItemEqualList(tuple(args)), **kwargs)

            except Exception as e:
                e.add_note(
                    f"^ occurred in {method.__name__} (mod: {method.__module__})"
                )
                raise e

        return decor

    def __validate_method(cls, instance: BaseNode, constructor):
        exceptions: list[Exception] = []

        # check class attributes
        if not ("_lines" in instance.__slots__):
            err = AttributeError(
                f"{type(instance).__name__!r} must have an attribute _lines"
            )
            exceptions.append(err)

        if not ("_line_range" in instance.__slots__):
            err = AttributeError(
                f"{type(instance).__name__!r} must have an attribute _line_range"
            )
            exceptions.append(err)

        # check constructor parameters
        if "lines" in constructor.__annotations__:
            err = ArgumentError(
                f"{type(instance).__name__}.__init__ takes in deprecated param lines"
            )
            exceptions.append(err)

        if "line_range" in constructor.__annotations__:
            err = ArgumentError(
                f"{type(instance).__name__}.__init__ takes in deprecated param line_range"
            )
            exceptions.append(err)

        # check getters and setters
        if not ("line_range" in dir(instance)):
            exceptions.append(
                AttributeError(
                    f"{type(instance).__name__} must have a property line_range"
                )
            )

        if not ("lines" in dir(instance)):
            exceptions.append(
                AttributeError(f"{type(instance).__name__} must have a property lines")
            )

        # raise errors if there are any
        if exceptions:
            raise ExceptionGroup(
                f"{type(instance).__name__} failed to pass inspection", exceptions
            )

    def __validate_input(cls, func, args, kwargs):
        exceptions = []

        if kwargs.get("lines"):
            exceptions.append(ArgumentError("Got unexpected parameter lines"))

        if kwargs.get("line_range"):
            exceptions.append(ArgumentError("Got unexpected parameter line_range"))

        if exceptions:
            raise ExceptionGroup(
                f"Bad parameters passed to {func.__name__}", exceptions
            )
