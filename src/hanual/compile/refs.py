class Ref:
    def __init__(self, of: str) -> None:
        self.ref = of

    def __repr__(self) -> str:
        return f"REF[{self.ref}]"

    def __class_getitem__(cls, of: str):
        return cls(of)
