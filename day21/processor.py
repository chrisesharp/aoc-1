from opcodes import Opcode


class CPU:
    def __init__(self, op_table=None):
        self.registers = [0, 0, 0, 0, 0, 0]
        self.op_table = op_table
        self.program = None
        self.debug = False
        self.ipc = -1

    def fetch(self, ip):
        if self.ipc >= 0:
            self.registers[self.ipc] = ip
        return [int(x) for x in self.program[ip].split(' ')]

    def execute(self, instruction):
        opcode, A, B, C = instruction
        op = self.op_table[opcode].name
        func = getattr(self, op)
        if self.debug:
            print(self.registers, op, A, B, C)
        func(A, B, C)

    def matches(self, instruction, result):
        opcode, A, B, C = instruction
        ops = set()
        starting_reg = self.registers[:]
        for op in Opcode.__members__.keys():
            func = getattr(self, op)
            func(A, B, C)
            if self.registers == result:
                ops.add(op)
            self.registers = starting_reg[:]
        return {opcode: ops}

    def load(self, program):
        self.program = program

    def assemble(self):
        assembly = []
        for line in self.program:
            if line.find("#ip", 0) == 0:
                self.ipc = int(line[4])
                continue
            op_name = line[0:4]
            data = line[4:]
            optable = self.op_table.items()
            opc = [(num, op) for (num, op) in optable if op.name == op_name]
            instruction = str(opc[0][0]) + data
            assembly.append(instruction)
        self.program = assembly

    def run(self):
        highest_steps = 1846
        lowest_int = 7129803
        ip = 0
        execution_steps = 0
        while (self.valid_instruction_pointer(ip)):
            instruction = self.fetch(ip)
            self.execute(instruction)
            if self.result_compare_called(ip):
                if self.registers[4] != self.registers[0]:
                    return execution_steps, True
                else:
                    return execution_steps, False
            if self.ipc >= 0:
                ip = self.registers[self.ipc]
            if self.op_table[instruction[0]].name == "eqrr":
                print(execution_steps, ", reg ", self.registers[4])
                if self.registers[4] <= lowest_int and \
                        execution_steps >= highest_steps:
                    lowest_int = self.registers[4]
                    highest_steps = execution_steps
                    print("LOWEST", execution_steps, ", reg ", self.registers[4])
            ip += 1
            execution_steps += 1

    def run2(self):
        already_seen = set()
        cycle = []
        ip = 0
        execution_steps = 0
        while (self.valid_instruction_pointer(ip)):
            instruction = self.fetch(ip)
            self.execute(instruction)
            if self.result_compare_called(ip):
                if self.registers[4] in already_seen:
                    print("already seen ",self.registers[4], execution_steps)
                    return cycle.pop(), execution_steps
                else:
                    print("new: ",self.registers[4], "(",len(already_seen), ") over ", execution_steps)
                    already_seen.add(self.registers[4])
                    cycle.append(self.registers[4])
            if self.ipc >= 0:
                ip = self.registers[self.ipc]
            ip += 1
            execution_steps += 1
        return self.registers[4], execution_steps

    def valid_instruction_pointer(self, ip):
        return ip < len(self.program)

    def result_compare_called(self, ip):
        return ip == 28

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
    start_regs = [int(x) for x in lines[0][9:].replace(']', '').split(',')]
    instruction = [int(x) for x in lines[1].split(' ')]
    end_regs = [int(x) for x in lines[2][9:].replace(']', '').split(',')]
    return (start_regs, instruction, end_regs)


def analyse_samples(samples):
    opcode_samples = {}
    for sample in samples:
        start_regs, instruction, end_regs = interpret(sample)
        opcode = instruction[0]
        given_samples = opcode_samples.get(opcode, [])
        given_samples.append((start_regs, instruction, end_regs))
        opcode_samples.update({opcode: given_samples})
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
    finished = True
    for _, matches in opcode_matches.items():
        if len(matches) == 1:
            match = list(matches)[0]
            definites.append(match)
        else:
            finished = False
    return definites, finished


def rationalise(opcode_matches, definites):
    for opcode, matches in opcode_matches.items():
        if len(matches) > 1:
            already_assigned = matches.intersection(definites)
            if already_assigned:
                matches.discard(already_assigned.pop())
                opcode_matches.update({opcode: matches})


def create_opcode_table(input):
    samples = input.split("\n\n")

    opcode_samples = analyse_samples(samples)
    opcode_matches, _ = find_matches(opcode_samples)

    finished = False
    while(not finished):
        definites, finished = get_definites(opcode_matches)
        rationalise(opcode_matches, definites)

    op_table = {}
    for opcode, op in enumerate(definites):
        op_table[opcode] = Opcode[op]

    return op_table


def main(input, program):
    part1 = False
    op_table = create_opcode_table(input)
    cpu = CPU(op_table)

    cpu.load(program)
    cpu.assemble()
    if part1:
        print("Part 1:")
        searching = True
        start = 7120000
        while (searching):
            cpu.registers = [start, 0, 0, 0, 0, 0]
            steps, searching = cpu.run()
            if not searching:
                print("start = ", start, ", steps = ", steps)
            elif (start % 1000) == 0:
                print(start)
            start += 1
    else:
        print("Part 2:")
        #start = 4120
        start = 0
        cpu.registers = [start, 0, 0, 0, 0, 0]
        start, steps = cpu.run2()
        print("start = ", start, ", steps = ", steps)

    print("Answer: ", cpu.registers[0])


if __name__ == "__main__":
    with open("samples.txt", 'r') as myfile:
        samples = myfile.read()
    with open("program.txt", 'r') as myfile:
        program = myfile.readlines()
    main(samples, program)
