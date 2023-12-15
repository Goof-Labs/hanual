from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Generator

from hanual.lang.util.line_range import LineRange

from hanual.util import Reply, Response, Request, ArgumentError


class _BaseNodeMeta(ABCMeta):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance.__init__ = cls.__override_init(instance, method=instance.__init__)
        return instance

    def __override_init(cls, method):
        # This __init__ overrides the one in the class constructor; this is to inject a check to ensure that the
        # class can function correctly.
        # I am making this to help find bugs early when the class is defined, not when the code it is an object
        # floating around
        def __init__(self, *args, **kwargs):
            cls.__validate_input(method, args, kwargs)
            cls.__validate(self, method)

            self._lines = ""
            self._line_range = LineRange(-1, -1)

            method(self, *args, **kwargs)

        return __init__

    def __validate(cls, instance: BaseNode, constructor):
        exceptions: list[Exception] = []

        # check class attributes
        if not ("_lines" in instance.__slots__):
            err = AttributeError(f"{type(instance).__name__!r} must have an attribute _lines")
            exceptions.append(err)

        if not ("_line_range" in instance.__slots__):
            err = AttributeError(f"{type(instance).__name__!r} must have an attribute _line_range")
            exceptions.append(err)

        # check constructor parameters
        if "lines" in constructor.__annotations__:
            err = ArgumentError(f"{type(instance).__name__}.__init__ takes in deprecated param lines")
            exceptions.append(err)

        if "line_range" in constructor.__annotations__:
            err = ArgumentError(f"{type(instance).__name__}.__init__ takes in deprecated param line_range")
            exceptions.append(err)

        # check getters and setters
        if not ("line_range" in dir(instance)):
            exceptions.append(AttributeError(f"{type(instance).__name__} must have a property line_range"))

        if not ("lines" in dir(instance)):
            exceptions.append(AttributeError(f"{type(instance).__name__} must have a property lines"))

        # raise errors if there are any
        if exceptions:
            raise ExceptionGroup(f"{type(instance).__name__} failed to pass inspection", exceptions)

    def __validate_input(cls, func, args, kwargs):
        exceptions = []

        if kwargs.get("lines"):
            exceptions.append(ArgumentError("Got unexpected parameter lines"))

        if kwargs.get("line_range"):
            exceptions.append(ArgumentError("Got unexpected parameter line_range"))

        if exceptions:
            raise ExceptionGroup(f"Bad parameters passed to {func.__name__}", exceptions)


class BaseNode(metaclass=_BaseNodeMeta):
    __slots__ = (
        "_lines",
        "_line_range",
    )

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def prepare(self) -> Generator[Response | Request, Reply, None]:
        """Used to collect information from the node.

        > Provides all necessary info to the compiler such as variable names and
        > constants.

        @return^Generator[Response | Request, Reply, None]>A gen that provides information to the compiler.
        | This gen takes in a compiler Reply and yields either a Request or a reply.
        | The gen should yield data or a request to the compiler and take a reply
        | in this sense, this gen is bidirectional.
        """
        raise NotImplementedError

    @abstractmethod
    def gen_code(self):
        """Generates the code for the compiler to omit.

        """
        raise NotImplementedError

    @property
    def lines(self) -> str:
        return self._lines

    @lines.setter
    def lines(self, new: str) -> None:
        assert isinstance(new, str), "new value for lines must be a str"
        self._lines = new

    @property
    def line_range(self) -> LineRange:
        return self._line_range

    @line_range.setter
    def line_range(self, new: LineRange) -> None:
        assert isinstance(new, LineRange), "new value must be a line_range"
        self._line_range = new
