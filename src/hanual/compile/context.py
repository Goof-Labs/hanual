from __future__ import annotations

from typing import Type

from hanual.util.equal_list import ItemEqualList


class Context:
    def __init__(self, *, deleter, getter, intents=None, _empty: bool = False):
        self._empty = _empty

        if _empty:
            return

        self._deleter = deleter
        self._getter = getter

        self._options: dict[str, object] = {}

        if intents is None:
            intents = []

        self.intents = ItemEqualList(intents)

    def __enter__(self):
        if self._empty:
            raise Exception("Can't do this on an empty context")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._empty:
            raise Exception("Can't do this on an empty context")

        del self

    def add_intents(self, *intents):
        if self._empty:
            raise Exception("Can't do this on an empty context")

        self.intents.extend(intents)

    def add(self, *args, **kwargs):
        if self._empty:
            raise Exception("Can't do this on an empty context")

        if (not args) and (not kwargs):
            raise Exception(f"No parameters passed")

        if set(args) & set(kwargs):
            raise Exception(f"Duplicated params {set(args) & set(kwargs)}")

        self._options.update(kwargs)

    def get(self, inf, recursive: bool = False) -> object | None:
        if self._empty:
            raise Exception("Can't do this on an empty context")

        if recursive:
            return list(set(self._get_recursive(inf)))

        key: object = self._options.get(inf, None)

        if key is not None:
            return key

        return None

    def get_intents_recursive(self):
        for ctx in self._getter():
            yield from ctx.intents

    def _get_recursive(self, inf):
        for context in self._getter():  # get all contexts
            res = context.get(inf)

            if res:
                yield res

    def assert_instance(self, option: str, *cls: Type):
        if self._empty:
            raise Exception("Can't do this on an empty context")

        key = self._options.get(option, None)

        if key is None:
            return False

        return isinstance(key, cls)

    def __str__(self):
        if self._empty:
            return f"Context(EMPTY)"

        return f"Context({self._options=} {self.intents=})"

    def __repr__(self):
        return str(self)

    @classmethod
    def make_empty(cls):
        return Context(deleter=None, adder=None, getter=None, _empty=True)
