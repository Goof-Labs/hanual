# Nim VM, Virtual machine for compiling and interepreting the hanual bytecode. It is speedy as nim is complied to C.
# !! DO NOT CHANGE THIS UNLESS YOU KNOW WHAT YOU'RE DOING !!
# ok

type
    instructions = enum
    


#[
    !!
    I have removed memory management for now as the only things I can find on it is that it is 'managed by nim'. I'll do something about it tomorrow.
    Also yes I am perfectly aware that this code makes no sense and you're probably thinking what the fudge am I doing.
    I have a plan. I am also aware that that sounds very sketchy and unreliable...
    !! 
]#

# Parse file into various parts (Instruction, const, etc. pools)
let file2parse = readFile("thereallylongfilethatiscool.chnl")

for instructions in somerandomfile:
    case instructions:
        of NOP:
            ...
        of JMP:
            ...
        of JEZ:
            ...
        of JNZ:
            ...
        of JIE:
            ...
        of SWP:
            ...
        of YNK:
            ...
        of PP1:
            ...
        of PP2:
            ...
        of PP3:
            ...
        of PGV:
            ...
        of PGC:
            ...
        of PGA:
            ...
        of PK1:
            ...
        of PK2:
            ...
        of PK3:
            ...
        of PK4:
            ...
        of PK5:
            ...
        of PKN:
            ...
        of RZE:
            ...
        of CAL:
            ...
        of RET:
            ...

#[
Hello, in repsonse to the message you left above, I am all ok with the current state of the code,
I get that you want to update it so thanks for the heads up. The below table is for how constants
are stored in the code, constants are just loaded onto the stack and can be mutated or whatever.

strings |>  Strings are stored with the ascii characters, so HI would be 48 49 Strings are
            separated by a 0 byte, currentelly there is no escaping so all is ok.

Number  |>  Numbers, numbers are stored in the same way as character, these can also be a maximum
            of one byte so a max of 255

Floats  |>  Floats are somewhat of a pain, but luckilly a float can be represented as a fraction
            this has soo many benifits, such as these can be loaded lazilly. Take the float 0.5
            in a fraction we could represent this as 1/2 so 1 would be the first byte and the
            second one would be 2 because that is the denominator of this fraction.

Also you differentate all of these by the first byte. If the first byte of the constant is a
number from 0 to 2 (inclusive). 0 is an intager, 1 is a string and 2 is a float.

so If we had the stream of bytes (These are hex):
00 00 00 00 48 45 4C 4C 4F 00 01 FF 00 02 01 02 00 00 00

At first this string may feel like chaos. But lets take a deeper look. In total there are 3 constants
(this is defined in the header) the first 3 00 bytes are for padding, so just omit the [ 00 00 00 ]
then the first byte of the first constant is 00 which tells us how to interperate the constant, in
this case the 00 byte matches up with the string type. So the following bytes [ 48 45 4C 4C 4F ] are
ascii values for a string, (also note we remove the first byte that tells use how to use the next
bytes). Then we have a pading 00 byte, so this must be the next constant, the first byte is a 01
so this must be an intager, reading the next byte wich is FF is 255 in decimal so we would just load
this as is. EZ. Last we have another padding byte with a 02 this is a float, so we then load the 01
which is the numarator and then the 02 which is the denominator, then we devide the first byte by the
second byte to get the float value. Then we have our last 3 padding 0s so this is the end of the
constant pool.

The header is the first 20 or so bytes of the file, you can just straitup read them and dump them into
a file, you may want to validate stuff like the magic number though first. also the number on the right
is how manny bytes in size it is.
4  - The fiurst 4 bytes are the magic number in this case the ascii codes for LMAO or 4C 4D 41 4F
44 - This is the checksum which is b64 encoded, this is just a hash of the source, (btw if we used
     the normal sha256 hexdegest the length would be 64 characters long, so saved 22 bytes)
1  - The majour version v1 or v2 or v3 and  so on, this is just the number
1  - This is the minor revision so v1.1 v1.2 v1.3
1  - This is the micro so version v1.0.1 v1.0.2 v1.0.3
1  - This byte tells us how manny constants are in the constant pool

I would also just start parsing the const pool and header, also the hash or checksum is to compress
the source code, not to check if the bytecode has been changed. This lets the compiler not need to
run if an old version of the compiled file is already up to date, do send me a message on discord if
you want to use a bytecode check sum too.
]#
