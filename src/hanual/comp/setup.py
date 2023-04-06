with open("test.txt", "wb") as f:
    f.write(b"LOL")  # magic

    f.write(b"\x01")  # maj
    f.write(b"\x00")  # min

    f.write(b"\x00")  # numconsts
    f.write(b"\x02")

    f.write(b"\xAA")  # metta data 1
    f.write(b"\x01")  # const 1

    f.write(b"\x00")

    f.write(b"\xAA")  # metta data 2
    f.write(b"\001")  # const 2

    f.write(b"\x00")

    f.write(b"\xFF")
    f.write(b"\xFF")
    f.write(b"\xFF")
    f.write(b"\xFF")

    f.write(b"\x00")
    f.write(b"\x00")
    f.write(b"\x00")
    f.write(b"\x00")
    f.write(b"\x00")
    f.write(b"test")
