class Constant:
    def __init__(self, value) -> None:
        self.value = value

    def serialize(self):
        if isinstance(self.value, int):
            return b"\x02" + b"\x00" + self.value.to_bytes(length=8, byteorder="big")

        elif isinstance(self.value, float):
            a, b = self.value.as_integer_ratio()
            return (
                b"\x03"
                + b"\x00"
                + a.to_bytes(length=8, byteorder="big")
                + b"\x00"
                + b.to_bytes(length=8, byteorder="big")
            )

        elif isinstance(self.value, str):
            return b"\x01" + b"\x00" + self.value.encode("ascii")

        else:
            raise NotImplementedError
