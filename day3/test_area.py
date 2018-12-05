from claim import Claim

def test_1():
    claim = Claim()
    input = ["#1 @ 1,3: 2x2"]
    claim.parse(input)
    area = {(1,3),(2,3),(1,4),(2,4)}
    assert claim.area("#1") == area

def test_2():
    claim = Claim()
    input = ["#1 @ 2,3: 2x2"]
    claim.parse(input)
    area = {(2,3),(3,3),(2,4),(3,4)}
    assert claim.area("#1") == area

def test_3():
    claim = Claim()
    input = ["#1 @ 2,3: 2x2"]
    area = {(2,3),(3,3),(2,4),(3,4)}
    claim.parse(input)
    assert claim.area("#1") == area

def test_4():
    file = open("test2.txt", "r")
    claim = Claim()
    claim.parse(file)
    (overlap, unique) = claim.calculate()
    assert overlap == 4
    assert unique == {"#3"}