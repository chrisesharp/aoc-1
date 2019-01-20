from processor import CPU

def test_addr():
    cpu = CPU()
    cpu.registers = [1,0,1,0]
    cpu.addr(0,2,3)
    assert cpu.registers == [1,0,1,2]

def test_addi():
    cpu = CPU()
    cpu.registers = [1,0,1,0]
    cpu.addi(0,2,3)
    assert cpu.registers == [1,0,1,3]

def test_mulr():
    cpu = CPU()
    cpu.registers = [2,3,0,0]
    cpu.mulr(0,1,2)
    assert cpu.registers == [2,3,6,0]
    
    cpu.registers = [3,2,1,1]
    cpu.mulr(2,1,2)
    assert cpu.registers == [3,2,2,1]

def test_muli():
    cpu = CPU()
    cpu.registers = [2,3,0,0]
    cpu.muli(0,1,2)
    assert cpu.registers == [2,3,2,0]

def test_banr():
    cpu = CPU()
    cpu.registers = [0,128,255,0]
    cpu.banr(1,2,3)
    assert cpu.registers == [0,128,255,128]

def test_bani():
    cpu = CPU()
    cpu.registers = [0,128,255,0]
    cpu.bani(1,255,3)
    assert cpu.registers == [0,128,255,128]

def test_borr():
    cpu = CPU()
    cpu.registers = [0,128,255,0]
    cpu.borr(1,2,3)
    assert cpu.registers == [0,128,255,255]

def test_bori():
    cpu = CPU()
    cpu.registers = [0,128,0,0]
    cpu.bori(1,255,3)
    assert cpu.registers == [0,128,0,255]

def test_setr():
    cpu = CPU()
    cpu.registers = [0,128,0,0]
    cpu.setr(1,255,3)
    assert cpu.registers == [0,128,0,128]

def test_seti():
    cpu = CPU()
    cpu.registers = [0,32,0,0]
    cpu.seti(1,255,3)
    assert cpu.registers == [0,32,0,1]

def test_gtir():
    cpu = CPU()
    cpu.registers = [0,32,0,0]
    cpu.gtir(33,1,3)
    assert cpu.registers == [0,32,0,1]
    cpu.gtir(31,1,3)
    assert cpu.registers == [0,32,0,0]

def test_gtri():
    cpu = CPU()
    cpu.registers = [0,32,0,0]
    cpu.gtri(1,31,3)
    assert cpu.registers == [0,32,0,1]
    cpu.gtri(1,33,3)
    assert cpu.registers == [0,32,0,0]

def test_gtrr():
    cpu = CPU()
    cpu.registers = [31,32,33,0]
    cpu.gtrr(2,1,3)
    assert cpu.registers == [31,32,33,1]
    cpu.gtrr(1,1,3)
    assert cpu.registers == [31,32,33,0]

def test_eqir():
    cpu = CPU()
    cpu.registers = [0,32,0,0]
    cpu.eqir(32,1,3)
    assert cpu.registers == [0,32,0,1]
    cpu.eqir(33,1,3)
    assert cpu.registers == [0,32,0,0]

def test_eqri():
    cpu = CPU()
    cpu.registers = [0,32,30,0]
    cpu.eqri(1,32,3)
    assert cpu.registers == [0,32,30,1]
    cpu.eqri(2,32,3)
    assert cpu.registers == [0,32,30,0]

def test_eqrr():
    cpu = CPU()
    cpu.registers = [0,32,32,0]
    cpu.eqrr(1,2,3)
    assert cpu.registers == [0,32,32,1]
    cpu.eqrr(0,1,3)
    assert cpu.registers == [0,32,32,0]