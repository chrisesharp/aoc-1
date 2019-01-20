from opcodes import Opcode
import sys

class CPU:
    def __init__(self, op_table=None):
        self.registers = [0,0,0,0]
        self.op_table = op_table
        self.program = None
        self.debug = False
    
    def execute(self, instruction):
        opcode, A, B, C = instruction
        op = self.op_table[opcode].name
        func = getattr(self, op)
        if self.debug: print(self.registers,op,A,B,C)
        func(A,B,C)
    
    def matches(self, instruction, result):
        opcode, A, B, C = instruction
        ops = set()
        starting_reg = self.registers[:]
        for op in Opcode.__members__.keys():
            func = getattr(self, op)
            func(A,B,C)
            if self.registers == result:
                ops.add(op)
            self.registers = starting_reg[:]
        return {opcode:ops}
    
    def load(self, program):
        self.program = program
        
    def run(self):
        for line in self.program:
            instruction = [int(x) for x in line.split(' ')]
            self.execute(instruction)
        
    
    def addr(self, A, B, C):
        self.registers[C] = self.registers[A] + self.registers[B]

    def addi(self, A, B, C):
        self.registers[C] = self.registers[A] + B

    def mulr(self, A, B, C):
        self.registers[C] = self.registers[A] * self.registers[B]

    def muli(self, A, B, C):
        self.registers[C] = self.registers[A] * B

    def banr(self, A, B, C):
        self.registers[C] = self.registers[A] & self.registers[B]

    def bani(self, A, B, C):
        self.registers[C] = self.registers[A] & B

    def borr(self, A, B, C):
        self.registers[C] = self.registers[A] | self.registers[B]

    def bori(self, A, B, C):
        self.registers[C] = self.registers[A] | B

    def setr(self, A, B, C):
        self.registers[C] = self.registers[A]

    def seti(self, A, B, C):
        self.registers[C] = A

    def gtir(self, A, B, C):
        self.registers[C] = (A > self.registers[B]) and 1 or 0

    def gtri(self, A, B, C):
        self.registers[C] = (self.registers[A] > B) and 1 or 0

    def gtrr(self, A, B, C):
        self.registers[C] = (self.registers[A] > self.registers[B]) and 1 or 0

    def eqir(self, A, B, C):
        self.registers[C] = (A == self.registers[B]) and 1 or 0

    def eqri(self, A, B, C):
        self.registers[C] = (self.registers[A] == B) and 1 or 0

    def eqrr(self, A, B, C):
        self.registers[C] = (self.registers[A] == self.registers[B]) and 1 or 0

def interpret(input):
    lines = [x.strip() for x in input.split("\n")]
    start_regs = [int(x) for x in lines[0][9:].replace(']','').split(',')]
    instruction = [int(x) for x in lines[1].split(' ')]
    end_regs = [int(x) for x in lines[2][9:].replace(']','').split(',')]
    return (start_regs, instruction, end_regs)

def analyse_samples(samples):
    opcode_samples = {}
    for sample in samples:
        start_regs, instruction,end_regs = interpret(sample)
        opcode = instruction[0]
        given_samples = opcode_samples.get(opcode,[])
        given_samples.append((start_regs, instruction, end_regs))
        opcode_samples.update({opcode:given_samples})
    return opcode_samples

def find_matches(opcode_samples):
    cpu = CPU()
    opcode_matches = {}
    count_three_or_more = 0
    for opcode, samples in sorted(opcode_samples.items()):
        for sample in samples:
            start_regs, instruction, end_regs = sample
            cpu.registers = start_regs
            matches = cpu.matches(instruction, end_regs)
            set_of_ops = matches[opcode]
            if len(set_of_ops) > 2:
                count_three_or_more += 1
            acc_set = opcode_matches.get(opcode, None)
            if acc_set:
                acc_set = acc_set.intersection(set_of_ops)
            else:
                acc_set = set(set_of_ops)
            opcode_matches[opcode] = acc_set
    return opcode_matches, count_three_or_more

def get_definites(opcode_matches):
    definites = []
    finished=True
    for opcode, matches in opcode_matches.items():
        if len(matches) == 1:
            match = list(matches)[0]
            definites.append(match)
        else:
            finished=False
    return definites, finished

def rationalise(opcode_matches, definites):
    for opcode, matches in opcode_matches.items():
        if len(matches) > 1:
            already_assigned = matches.intersection(definites)
            if already_assigned:
                matches.discard(already_assigned.pop())
                opcode_matches.update({opcode:matches})

def main(input, program):
    print("Part 1:")
    samples = input.split("\n\n")
    
    opcode_samples = analyse_samples(samples)
    opcode_matches, count_three_or_more = find_matches(opcode_samples)


    print("Num of samples matching 3 or more ops: ", count_three_or_more)
    print("===============")
    print("Part 2:")
    
    finished=False
    while(not finished):
        definites, finished = get_definites(opcode_matches)
        rationalise(opcode_matches, definites)

    op_table = {}
    for opcode, op in enumerate(definites):
        op_table[opcode] = Opcode[op]

    cpu = CPU(op_table)
    cpu.load(program)
    cpu.run()
    
    print("Answer: ",cpu.registers[0])

if __name__ == "__main__":
    with open("input1.txt", 'r') as myfile:
        input1 = myfile.read()
    with open("input2.txt", 'r') as myfile:
        input2 = myfile.readlines()
    main(input1,input2)
