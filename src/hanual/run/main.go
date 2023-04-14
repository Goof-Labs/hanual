package main

import (
	"io/ioutil"
	"log"
)

func main() {
	bytes, err := ioutil.ReadFile("test.txt")

	if err != nil {
		log.Panic("failed to read: ", err)
	}

	ff := FromBytes(bytes)
	pprint(*ff)
}
