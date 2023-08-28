from __future__ import annotations


from hanual.compile.compile_manager import CompileManager


class Ref:
    def __init__(self, of: str) -> None:
        self.ref = of

    def compile(self, cm: CompileManager):
        return cm.names.index(self.ref)

    def __repr__(self) -> str:
        return f"REF[{self.ref}]"

    def __class_getitem__(cls, of) -> Ref:
        return cls(of[0])
