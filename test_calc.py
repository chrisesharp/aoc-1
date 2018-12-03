from calc import answer

def test_1():
    file = open("test1.txt", "r")
    assert answer(file) == 3
    
def test_2():
    file = open("test2.txt", "r")
    assert answer(file) == 0
    
def test_3():
    file = open("test3.txt", "r")
    assert answer(file) == -6