from __future__ import annotations


class Intent:
    __slots__ = "_name", "_value"

    def __init__(self, name=""):
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def __eq__(self, other: object):
        if not isinstance(other, Intent):
            raise Exception(
                f"other in op == must be an intent, got {type(other).__name__}"
            )

        return self.name == other.name

    def __str__(self):
        return f"{type(self).__name__}({self.name=})"

    def __repr__(self):
        return str(self)
