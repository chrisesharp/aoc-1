from license import lic, lic2

def test_0():
    input = "0 3 1 1 2"
    sum = lic(0,input.split(' '),0)
    assert sum[0] == 4

def test_1():
    input = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    sum = lic(0, input.split(' '),0)
    assert sum[0] == 138

def test_2():
    input = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    sum = lic2(0, input.split(' '),0)
    assert sum[0] == 66