package main

import (
	"container/list"
)

type HanualConstant struct {
	bytes  []byte
	format uint8
}

type HanualFileFormat struct {
	magic     [3]byte // aka 3 chars
	major     uint8
	minor     uint8
	const_len uint32
	consts    list.List
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
		format: Type,
		bytes:  DataBytes,
	}
}
