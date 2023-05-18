# Nim VM, Virtual machine for compiling and interepreting the hanual bytecode. It is speedy as nim is complied to C.
# !! DO NOT CHANGE THIS UNLESS YOU KNOW WHAT YOU'RE DOING !!
# ok

type
    instructions = enum
        NOP = 0b0000_0000,
    
        JMP = 0b1110_0000,  # unconditional Jump
        JEZ = 0b1110_0001,  # Jump if 0
        JNZ = 0b1110_0010,  # Jump not 0
        JIE = 0b1110_0011,  # jump if error
    
        SWP = 0b0100_1000,  # swap top two elements
        YNK = 0b1100_1100,  # yank n'th element and push it to top
    
        PP1 = 0b0100_0000,  # Pops top element
        PP2 = 0b0100_0001,  # Pops two elements of stack
        PP3 = 0b0100_0010,  # pops three elements of stack
    
        PGV = 0b1100_0000,  # Push global value on stack
        PGC = 0b1100_0001,  # Push constant onto stack
        PGA = 0b1100_0010,  # Push global address, e.g. function
    
        PK2 = 0b0100_0010,  # Pack top 2 elements into tuple
        PK3 = 0b0100_0011,  # Pack top 3 elements into tuple
        PK4 = 0b0100_0100,  # Pack top 4 elements into tuple
        PK5 = 0b0100_0101,  # Pack top 5 elements into tuple
        PKN = 0b1100_1000,  # Pack top n elements into tuple
        PK1 = 0b0100_1001,  # Pack first value into tuple, (I forgot to add this in earlier, so now it exists)
    
        RZE = 0b0100_0000,  # Raise Exception
        
        CAL = 0b0100_0001,  # Call function
        RET = 0b0000_0001  # return


#[
    !!
    I have removed memory management for now as the only things I can find on it is that it is 'managed by nim'. I'll do something about it tomorrow.
    Also yes I am perfectly aware that this code makes no sense and you're probably thinking what the fudge am I doing.
    I have a plan. I am also aware that that sounds very sketchy and unreliable...
    !! 
]#

# Parse file into various parts (Instruction, const, etc. pools)

let file2parse = readFile("thereallylongfilethatiscool.chnl")

func parse_file(): return type =
    ...


for instructions in somerandomfile:
    instructions.NOP