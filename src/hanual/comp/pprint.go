package main

func pprint(targ HanualFileFormat) {
	println("magic = ", string(targ.magic[:]))
	println("major = ", targ.major)
	println("minor = ", targ.minor)
	println("const len = ", targ.const_len)
	println("const num = ", targ.consts.Len())

	for i := targ.consts.Front(); i != nil; i = i.Next() {
		println("- ", i.Value.(*HanualConstant).format)
		println("- ", i.Value.(*HanualConstant).bytes)
	}
}
