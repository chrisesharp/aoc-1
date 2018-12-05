from scanner import Scanner

def test_1():
    scanner = Scanner()
    file = open("test1.txt", "r")
    assert scanner.checksum(file) == 0

def test_2():
    scanner = Scanner()
    file = open("test2.txt", "r")
    assert scanner.checksum(file) == 1
    
def test_3():
    scanner = Scanner()
    file = open("test3.txt", "r")
    assert scanner.checksum(file) == 12

def test_4():
    scanner = Scanner()
    file = open("test4.txt", "r")
    scanner.checksum(file)
    assert scanner.common() == "fgij"