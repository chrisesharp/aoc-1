from calc import Calc

def test_1():
    calc = Calc()
    file = open("test1.txt", "r")
    assert calc.answer(file) == 3
    
def test_2():
    calc = Calc()
    file = open("test2.txt", "r")
    assert calc.answer(file) == 0
    
def test_3():
    calc = Calc()
    file = open("test3.txt", "r")
    assert calc.answer(file) == -6
    
def test_4():
    calc = Calc()
    file = open("test4.txt", "r")
    assert calc.answer(file) == 0
    assert calc.repeating_freq() == 0

def test_5():
    calc = Calc()
    file = open("test5.txt", "r")
    assert calc.answer(file) == 4
    assert calc.repeating_freq() == 10
    
def test_6():
    calc = Calc()
    file = open("test6.txt", "r")
    assert calc.answer(file) == 4
    assert calc.repeating_freq() == 5