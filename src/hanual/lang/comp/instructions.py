from enum import Enum


"""
Each instruction is a byte so thare are a possible of 256 possible instructions.
The Instruction set can be devided into two catagories, ones which require an
operan aka argument. And ones which dont require one. By using some bit fiddeling
we can have the most significant byte, first bit, be like a flag where a 1
represents it requiring a second operator and a 0 is no nest operator required.

ABCD
vvvv
0000 0000
    |----|
This part is to separate the starting arguments from indevidual operators unless
specified otherwise.


A => The most significant bit indecates if the next byte should be loaded as an operang.
B => Stack Change
C => Hop, if we are hopping to another instruction
D => Reserved, set to 0
"""

class Instructions(Enum):
    # I have used the underscore to separate the two nibbles
    NOP = 0b0000_0000

    JMP = 0b1110_0000 # unconditional Jump
    JEZ = 0b1110_0001 # Jump if 0
    JNZ = 0b1110_0010 # Jump not 0
    JIE = 0b1110_0011 # jump if error

    PP1 = 0b0100_0000 # Pops top element
    PP2 = 0b0100_0001 # Pops two elements of stack
    PP3 = 0b0100_0010 # pops three elements of stack

    PGV = 0b1100_0000 # Push global value on stack
    PGC = 0b1100_0001 # Push constant onto stack
    PGA = 0b1100_0010 # Push global address, e.g function

    PK2 = 0b0100_0010 # Pack top 2 elements into tuple
    PK3 = 0b0100_0011 # Pack top 3 elements into tuple
    PK4 = 0b0100_0100 # Pack top 4 elements into tuple
    PK5 = 0b0100_0101 # Pack top 5 elements into tuple
    PKN = 0b1100_1000 # Pack top n elements into tuple

    RZE = 0b0100_0000 # Raise Eeception

    CAL = 0b0100_0001 # Call function

