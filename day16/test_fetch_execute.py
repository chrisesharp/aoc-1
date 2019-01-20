from processor import CPU, interpret
from opcodes import Opcode

def test_execute():
    input = """Before: [3, 2, 1, 1]
    9 2 1 2
    After:  [3, 2, 2, 1]
    """
    start_regs, instruction,end_regs = interpret(input)
    cpu = CPU({
                9: Opcode.mulr
                })
    cpu.registers = start_regs
    cpu.execute(instruction)
    assert cpu.registers == end_regs

def test_run():
    input = ["9 2 1 2","8 2 1 2"]
    cpu = CPU({
                8: Opcode.addr,
                9: Opcode.mulr
                })
    cpu.registers = [3, 2, 1, 1]
    cpu.load(input)
    cpu.run()
    assert cpu.registers == [3, 2, 4, 1]

def test_op_effects():
    input = """Before: [3, 2, 1, 1]
    9 2 1 2
    After:  [3, 2, 2, 1]
    """
    start_regs, instruction, end_regs = interpret(input)
    
    cpu = CPU()
    cpu.registers = start_regs
    matches = cpu.matches(instruction, end_regs)
    set_of_ops = matches[instruction[0]]
    expected = set((Opcode.mulr.name,Opcode.addi.name,Opcode.seti.name))
    assert set_of_ops == expected

