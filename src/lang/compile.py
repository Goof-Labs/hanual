import marshal
import types


ocode = compile("print('Hello wolrd')", "", "eval")


# for name in dir(ocode):
#    if not name.startswith("co_"):
#        continue
#
#    print(f"{name} = {getattr(ocode, name)!r}")


ccode = types.CodeType(
    0,
    0,
    0,
    0,
    3,
    0,
    b"\x97\x00\x02\x00e\x00d\x00\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00S\x00",
    ("Hello world", *("+" * i for i in range(10))),
    ("print",),
    (),
    "",
    "<module>",
    "<module>",
    1,
    b"\xf0\x03\x01\x01\x01\xd8\x00\x05\x80\x05\x80m\xd1\x00\x14\xd4\x00\x14\xd0\x00\x14",
    b"",
    (),
    (),
)


bcode = marshal.dumps(ccode)


print(ccode.co_code.hex())
print(bcode.index(ccode.co_code))

f = open("a.pyc", "wb")

marshal.dump(ccode, f)

f.close()
