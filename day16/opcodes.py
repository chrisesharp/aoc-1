from enum import Enum

class Opcode(Enum):
    addr = 0
    addi = 1
    mulr = 2
    muli = 3
    banr = 4
    bani = 5
    borr = 6
    bori = 7
    setr = 8
    seti = 9
    gtir = 10
    gtri = 11
    gtrr = 12
    eqir = 13
    eqri = 14
    eqrr = 15