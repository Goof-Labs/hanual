from hanual.lang.util.const_pool import ConstPoolMod, InterfaceConstPoolAdd
from hanual.lang.util.labels import Label, LabelInterface, VALUE
from hanual.lang.types.singelton import Singleton
from typing import Dict, Any
from sys import version_info
from abc import ABC


class HanualFileDumps(InterfaceConstPoolAdd, LabelInterface, ABC, Singleton):
    """
    This class is a singleton so to make an instance or get an instance you need to call `get_instance`, this will
    either create or get the class instance, this is so we can access this class from anywhere in the code without
    the class as a reference.
    The class implements several methods:
        - const_pool will return a ConstPoolMod class
        - labels will return a Label class
    """

    def __init__(self) -> None:
        self._const_pool = {}
        self._labels = {}

        self._idx = 0

    #  LABEL CONTROL

    def advance(self) -> None:
        self._idx += 1

    @property
    def get_idx(self) -> VALUE:
        return self._idx

    def const_pool(self):
        return ConstPoolMod[HanualFileDumps, Any](self)

    def labels(self):
        return Label[HanualFileDumps](self)

    # CONST CONTROL

    def add_consts(self, consts: Dict[str, Any], allow_override: bool = False) -> None:
        if not isinstance(consts, dict):
            raise TypeError(
                "expected type Dict[str, Any] got type %s",
                (type(consts).__name__,),
            )

        if not self._const_pool:
            self._const_pool = consts
            return

        for k, v in consts.items():
            assert isinstance(k, str)

            if allow_override:
                self._const_pool[k] = v

            else:
                if k in self._const_pool.keys():
                    err = KeyError(
                        "could not override key %s, the key is already in the constant pool"
                    )

                    if version_info.minor >= 11:
                        err.add_note("maby you want to mangle the name")

                    print("maby you want to mangle the name")

                    raise err
