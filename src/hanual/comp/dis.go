package main

import (
	"container/list"
)

type HanualInstruction struct {
	Idx         uint32
	LoadNext    bool
	StackChange bool
	HopToOther  bool
	id          uint8
	Next        *uint8 // or nil if next is not needed
	Raw         byte
}

type HanualConstantMettaData struct {
	primitive bool
	userDef   bool
	id        uint8 // lowest uint I could find, the id is a nibbel of data
}

type HanualConstant struct {
	bytes  []byte
	format *HanualConstantMettaData
}

type HanualFileFormat struct {
	magic        [3]byte // aka 3 chars
	major        uint8
	minor        uint8
	const_len    uint32
	consts       list.List
	instructions list.List
}

type FunctionStatus struct {
	msg string
	sts uint8
}

func FromBytes(bytes []byte) HanualFileFormat {
	magic := [3]byte{bytes[0], bytes[1], bytes[2]}

	// combine two bytes e.g 01011000 0101010 into a uint32 010110000101010
	var count uint32 = uint32(uint16(bytes[6]) | uint16(bytes[5])<<8)

	var fileformat = HanualFileFormat{
		magic:     magic,
		major:     bytes[3],
		minor:     bytes[4],
		const_len: uint32(count),
		consts:    *LoadConsts(&bytes, 7, uint16(count)),
	}

	return fileformat
}

//////////////////////////////////////////
///////////// LOAD CONSTANTS /////////////
//////////////////////////////////////////

func LoadConsts(bytes *[]byte, startfrom uint8, num_consts uint16) *list.List {
	constants := list.New()
	buildup := list.New()
	escape := false

	for _, byte_ := range (*bytes)[startfrom:] {

		if byte_ == 0 && !escape { // push buildup

			constants.PushBack(ProcessBytes(buildup))
			buildup = list.New() // clear buildup

		} else if byte_ == 0 && escape { // push escaped 0

			escape = false
			buildup.PushBack(byte_)

		} else if byte_ == 0xff && escape { // push escaped escape

			buildup.PushBack(byte_)
			escape = false

		} else if byte_ == 0xff && !escape { // set escaped to true

			escape = true

		} else { // just append the byte

			buildup.PushBack(byte_)

		}

	}

	return constants

}

func ProcessBytes(bytes *list.List) *HanualConstant {
	var Type uint8

	if MettaData := bytes.Front().Value; MettaData != nil {
		Type = uint8(MettaData.(uint8))
	}

	DataBytes := []byte{}

	for BByte := bytes.Front(); BByte != nil; BByte = BByte.Next() {
		DataBytes = append(DataBytes, BByte.Value.(uint8))
	}

	return &HanualConstant{
		format: ParseMettaDatta(Type),
		bytes:  DataBytes,
	}
}

func ParseMettaDatta(bytes byte) *HanualConstantMettaData {
	return &HanualConstantMettaData{
		primitive: ((bytes >> 7) & 0x0F) == 1, // get last bit, and conv to bool
		userDef:   ((bytes >> 6) & 0x0F) == 1, // get 2nd 2 last bit, then to bool
		id:        bytes & 0x0F,               // last nibbel of data
	}
}

////////////////////////////////////////////
/////////// PARSING INSTRUCTIONS ///////////
////////////////////////////////////////////

func ParseInstructionPool(pool *[]uint8, start uint32) *list.List {
	var idx uint32 = 0
	ippool := *pool

	instructions := list.New()

	var i uint32
	var f bool // break flag

	for {
		f = false

		for i = 0; i <= 5; i++ { // next 5 bytes are 0
			if ippool[idx+i] != 0 {
				f = true
				break
			}
		}

		if f { // next 5 bytes are 0 we break
			break
		}

		err, res := ParseInstruction(&ippool, &idx)

		if err != nil {
			// eof
			break
		}

		instructions.PushBack(res)
	}

	return instructions
}

func ParseInstruction(instructions *[]uint8, idx *uint32) (*FunctionStatus, *HanualInstruction) {
	(*idx)++ // increment to current instruction

	if int(*idx) < len(*instructions) {
		return &FunctionStatus{
			msg: "index out of bounds",
			sts: 1,
		}, nil
	}

	raw_instruction := (*instructions)[int(*idx)]

	var bytes [8]bool
	for i := uint8(0); i < 8; i++ {
		bytes[i] = (raw_instruction & (i << i)) != 0
	}

	instr := HanualInstruction{}

	instr.Idx = *idx
	instr.LoadNext = bytes[0]
	instr.StackChange = bytes[1]
	instr.HopToOther = bytes[2]

	if bytes[0] { // load next
		(*idx)++
		instr.Next = &(*instructions)[*idx]
	}

	instr.Raw = raw_instruction

	return nil, &instr
}
