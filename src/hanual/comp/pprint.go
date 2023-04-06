package main

func pprint(targ HanualFileFormat) {
	println("magic = ", string(targ.magic[:]))
	println("major = ", targ.major)
	println("minor = ", targ.minor)
	println("const len = ", targ.const_len)
	println("const num = ", targ.consts.Len())
	println("\nconsts\n")

	for i := targ.consts.Front(); i != nil; i = i.Next() {
		println(" BYTS = ", i.Value.(*HanualConstant).bytes)
		println(" MD-P = ", i.Value.(*HanualConstant).format.primitive)
		println(" MD-U = ", i.Value.(*HanualConstant).format.userDef)
		println(" MD-I = ", i.Value.(*HanualConstant).format.id)
		println()
	}

	println("\nend consts\n")

	println("\ninstructions\n")

	for ins := targ.instructions.Front(); ins != nil; ins = ins.Next() {
		i := *(ins.Value.(*HanualInstruction))

		println()
		println(" ID=", i.id)
		println(" HP=", i.HopToOther)
		println(" IX=", i.Idx)
		println(" NL=", i.LoadNext)
		println(" NX=", i.Next)
		println(" RW=", i.Raw)
		println(" NX=", i.StackChange)
	}

	println("\nend instructions\n")
}
