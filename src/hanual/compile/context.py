from __future__ import annotations


from typing import Type


class Context:
    def __init__(self, *, deleter, adder):
        self._deleter = deleter
        self._adder = adder

        self._mentioned = set()
        self._options = {}

    def __enter__(self):
        self._adder(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._deleter(self)

    def add(self, *args, **kwargs):
        if (not args) and (not kwargs):
            raise Exception(f"No parameters passed")

        if set(args) & set(kwargs):
            raise Exception(f"Duplicated params {set(args) & set(kwargs)}")

        self._mentioned = set(args) | set(kwargs)
        self._options = kwargs

    def get(self, inf):
        key = self._options.get(inf, None)

        if key is not None:
            return key

        if inf in self._mentioned:
            return True

        return None

    def assert_instance(self, option: str, *cls: Type):
        key = self._options.get(option, None)

        if key is None:
            return False

        return isinstance(key, cls)
