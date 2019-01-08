from recipes import Scoreboard

def test_1():
    scoreboard = Scoreboard(1)
    scoreboard.iterate(1)
    assert scoreboard.scores() == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1]


def test_2():
    scoreboard = Scoreboard(1)
    scoreboard.iterate(1)
    assert scoreboard.ten_recipes() == "7101012451"

def test_3():
    scoreboard = Scoreboard(5)
    scoreboard.iterate(5)
    assert scoreboard.ten_recipes() == "0124515891"

def test_4():
    scoreboard = Scoreboard(9)
    scoreboard.iterate(9)
    assert scoreboard.ten_recipes() == "5158916779"

def test_5():
    scoreboard = Scoreboard(1)
    pos = scoreboard.scan("5158916779",10000)
    assert pos == 9

def test_6():
    scoreboard = Scoreboard(1)
    pos = scoreboard.scan("92510",10000)
    assert pos == 18

def test_7():
    scoreboard = Scoreboard(1)
    pos = scoreboard.scan("59414",10000)
    assert pos == 2018
    