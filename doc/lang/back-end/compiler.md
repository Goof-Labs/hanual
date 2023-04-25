# Compiler

## Introduction

This language is compiled to a custom bytecode, with file size and speed in mind.

## File specification

| File                        |
|-----------------------------|
| Magic "LOL" as ascii bytes  |
| Major version 1 byte        |
| Minor version 1 byte        |
| Number of constants 2 bytes |
| Padding 0 byte              |
| Constants                   |
| Padding 0 byte              |
| Instructions                |
| 5 padding 0 bytes           |
| Metta data                  |

## Magic

The top level LOL bytes shows this file is useable by the hanual runtime.

## Major version

The majour version is the major version of the language with big features, this is a single byte which has an upper bound of 255 and a lower bound of 0.

## Minor version

The minor version is a small update to the software which will have strong backwaard compatability with the previous one. This is also a single byte with an upper and lower bound of 0 and 255 respectively.

This means that there is a maximum of 65,536 possible releases.

## Num constants

This is the number of constants in the constant pool. This is 2 bytes and counts how many constants are in the constants section.

## Constants

The constants are stored as raw bytes separated by a 0 byte, to escape the next byte, if it happens to be 0. We have a prefexing byte which is `1111 1111`. Each constant also starts with a metta byte, this byte provides some metta data about the following bytes and how to enterperate them.

The first bit of the metta byte is used to tell us if the following bytes are complex, (a primitive, e.g an int, string, char) or a complex, e.g. struct. 1 means that is complex, 0 is primitive.

The next bit is used to indicate if the type is user defined, 1 if yes 0, if no.

The next two bits are reserved and ae set to 0.

The last nibble is converted to an integer and tells us the index of the data type, if the type is user defined then it will check the constant pool, else it will look in the types reference table, to see what matches and how to use the bytes,

## Instructions

An instruction is one byte, the first byte describes the instruction, while the second byte, is a nunque ID used to separate them. This means that there are roughly 16 possible instructions that do roughly the same thing.

> Note: 1 means yes 0 means no. Just to clarifiy the next statements.

The first bit shows if the next byte should be used as an argument.

The next bit indicates if the instruction will affect the stack.

The next bit indicates if we ae hopping to another address or location in the code.

The fourth bit is set to 0, and is reserved.

The last nibble is a unique id for that category of instruction. So if we had several instructions that only changed the stack, we would need to differenciate between them, this means that we have a maximum of 16 possible instructions that have roughly the same effect.

## Metta data

This is to be decided.
