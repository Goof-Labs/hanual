from __future__ import annotations

from uuid import uuid4
from io import BytesIO


class Function:
    __slots__ = "_flags", "_name"

    def __init__(self, name: str, flags):
        self._flags = flags
        self._name = name
        self._init()

    def _init(self):
        if self._flags.get("private", False):
            self._flags["mangle"] = True

        if self._flags.get("mangle", False):
            self._name = "_" + uuid4().hex + "_" + self._name

    def comp(self):
        with BytesIO() as buffer:

            # TODO write stuff to buffer

            return {
                "code": buffer.getvalue(),
                "access": self._flags.get("private", False)
            }
