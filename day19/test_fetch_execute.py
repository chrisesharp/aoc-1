from processor import CPU, create_opcode_table


def test_non_ip():
    with open("samples.txt", 'r') as myfile:
        samples = myfile.read()
    with open("old_prog.txt", 'r') as myfile:
        program = myfile.readlines()
    op_table = create_opcode_table(samples)
    cpu = CPU(op_table)
    cpu.load(program)
    cpu.run()
    assert cpu.registers[0] == 503


def test_ip():
    program = [
        "#ip 0",
        "seti 5 0 1",
        "seti 6 0 2",
        "addi 0 1 0",
        "addr 1 2 3",
        "setr 1 0 0",
        "seti 8 0 4",
        "seti 9 0 5"
    ]

    with open("samples.txt", 'r') as myfile:
        samples = myfile.read()
    op_table = create_opcode_table(samples)
    cpu = CPU(op_table)

    cpu.load(program)
    cpu.assemble()
    cpu.run()

    assert cpu.registers == [6, 5, 6, 0, 0, 9]
