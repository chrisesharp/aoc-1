from power import power_level, Grid

def test_1():
    x, y = (3,5)
    sn = 8
    pwr = power_level(x,y,sn)
    assert pwr == 4

def test_2():
    x, y = (122, 79)
    sn = 57
    pwr = power_level(x,y,sn)
    assert pwr == -5

def test_3():
    x, y = (217, 196)
    sn = 39
    pwr = power_level(x,y,sn)
    assert pwr == 0

def test_4():
    x, y = (101, 153)
    sn = 71
    pwr = power_level(x,y,sn)
    assert pwr == 4

def test_5():
    grid = Grid(18)
    grid.powerup()
    assert grid.pwr_level((33,45)) == 4
    assert grid.pwr_level((34,45)) == 4
    assert grid.pwr_level((35,45)) == 4
    assert grid.pwr_level((33,46)) == 3
    assert grid.pwr_level((34,46)) == 3
    assert grid.pwr_level((35,46)) == 4
    assert grid.pwr_level((33,47)) == 1
    assert grid.pwr_level((34,47)) == 2
    assert grid.pwr_level((35,47)) == 4

def test_6():
    grid = Grid(18)
    grid.powerup()
    assert grid.pwr_square((33,45)) == 29

def test_7():
    grid = Grid(42)
    grid.powerup()
    assert grid.pwr_square((21,61)) == 30

def test_8():
    grid = Grid(18)
    grid.powerup()
    assert grid.pwr_square((90,269),16) == 113
    