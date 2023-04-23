from __future__ import annotations

from typing import TypeVar, List, Optional, Any, Generic, Union, Self, get_type_hints
from uuid import uuid1
from abc import ABC


T = TypeVar("T")

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class _ProductionInterface(ABC):
    def get(self, *args, **kwargs) -> T:
        raise NotImplementedError

    def __format__(self, format_spec: Any) -> None:
        pass


P = TypeVar("P", bound=_ProductionInterface)


class DefaultProduction(_ProductionInterface, ABC, Generic[A, B, C]):
    __slots__ = ("ts",)

    def __init__(self: Self, ts: List[T]) -> None:
        self.ts: List[T] = ts

    @property
    def raw(self) -> List[T]:
        return self.ts

    def __repr__(self: Self) -> str:
        return str(self.ts)

    def __getitem__(self: Self, item: int) -> Union[A, B, C]:
        return self.ts[item]


class ProductionGen(_ProductionInterface, ABC, Generic[A, B, C]):
    """
    This is a genorator production. This is one of many
    productions. Here we get elements out one after the
    other in a genorator like way.
    """

    def __init__(self: Self, tokens: List[T]) -> None:
        self.slice: List[T] = tokens
        self.idx = -1

    def next_token(self: Self) -> T:
        self.idx += 1
        return self.slice[self.idx]

    def back_token(self: Self) -> T:
        self.idx -= 1
        return self.slice[self.idx]

    def peek(self: Self) -> T:
        return self.slice[self.idx]

    def advance_idx(self: Self) -> None:
        self.idx += 1

    def back_idx(self: Self) -> None:
        self.idx -= 1

    def get_token_types(self: Self) -> List[str]:
        return list({t.type for t in self.slice})

    def get_len(self: Self) -> int:
        return len(self.slice)

    def __format__(self: Self, spec: str) -> str:
        """
        '%i' -> index of the production
        '%t' -> current token
        '%l' -> lenght
        '%r' -> raw tokens
        """
        string = ""

        encounter = False
        idx = -1

        while True:
            idx += 1

            try:
                char = spec[idx]

            except IndexError:
                break

            if encounter:
                if char == "i":
                    string += str(self.idx)

                elif char == "t":
                    string += str(self.peek())

                elif char == "l":
                    string += str(self.get_len())

                elif char == "r":
                    string += str(self.slice)

        return string


class ProductionDict(_ProductionInterface):
    def __init__(self: Self, tokens: List[T]) -> None:
        self._dct = {}
        appierence = {}
        # We want to keep track of how many times a token type appieres in total
        # This allows us to do
        # >>> prod.num1
        # >>> prod.num2
        # >>> prod.num3

        for t in tokens:
            if t.type in appierence.items():
                appierences = appierence.get(t.type, 0) + 1

                appierence[t.type] = appierences
                self._dct[f"{t.type.lower()}_{appierences}"] = t
                # We also lower case the token type so the token types look more pythonic

    def __getitem__(self: Self, __key: str) -> T:
        try:
            return self._dct[__key]

        except KeyError as e:
            # only py311+
            e.add_note(
                "Could not get key '%s', did you mean one of: %s",
                (__key, ", ".join(self._dct.keys())),
            )
            # display error message
            raise e

    def get(self: Self, key: str, default: Optional[Any] = None) -> None:
        return self._dct.get(key, default)


"""
NOT-WORKING

OrderElements are similar to TypeVar in the typing module. They allow you to
pass a variable arround as a type. However this is completely useless without
OrderProduction. This class is men to be used as below:
>>> A = OrderElement("A")
>>> B = OrderElement("B")
>>> C = OrderElement("C")
>>>
>>> def abc(ts: OrderProduction[A, B, C]):
>>>     return OrderProduction[C, B, A](abc, ts)

In the function can only take one paramiter, the token stream `ts`, this is
annotated similar to a `Generic` in typing. To define the return order we
return the production order with the `OrderElement` instances in a defferent
order. We then call this with the function and the token stream.

The OrderElement must have a `name` which is some sort of string. It is
recomended that these are assighned to a variable.

This saves you the inconvenience of accessing multiple index arrays at a time,
this is verry error prone, and not verry nice to deal with. So code that looks
like this:

>>> @par.rule("a b c")
>>> def abc(ts):
>>>     return ts[1], ts[0], ts[2]

Can be refactored into this:

>>> # at top level
>>> A = OrderElement("A")
>>> B = OrderElement("B")
>>> C = OrderElement("C")
>>> ...
>>> @par.rule("part_1 part_2 part_3")
>>> def some_rule(ts: OrderProduction[A, B, C]):
>>>     return OrderProduction[B, A, C](some_rule, ts)

NOTE: you only need to declare the `OrderElement` once at the top of the file.

Simply put: we declare several OrderElement instances, and pass them around
            `OrderProduction` s to rearange the order of elements.
"""


# Some things are best not explaned


class OrderElement:
    __slots__ = ("_id", "_nm")

    def __init__(self: Self, name: str) -> None:
        self._id = uuid1()
        self._nm = name


class OrderProduction:
    def _from_end(args):
        def inner(fn, ts):
            from_ = fn._args
            to = args

            join = {a._nm: b for a, b in zip(from_, ts)}
            print(" ".join(str(join.get(i._nm)) for i in to))

            return

        inner._args = args
        return inner

    def __class_getitem__(self: OrderProduction, paramiters):
        return self._from_end(paramiters)
