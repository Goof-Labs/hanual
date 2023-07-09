class _MettaGetAttr(type):
    def __getattribute__(self, __name: str):
        return self.__class_getattr__(cls=type(self), attr=__name)


class ClassGetAttr(metaclass=_MettaGetAttr):
    def __class_getattr__(self):
        raise NotImplementedError
