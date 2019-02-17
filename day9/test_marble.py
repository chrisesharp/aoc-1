from marble import Marble

def test_0():
    marble = Marble(2, 2)
    assert marble.place(1) == 1
    assert marble.place(2) == 1
    assert marble.place(3) == 3
    assert marble.place(4) == 1
    assert marble.place(5) == 3
    assert marble.place(6) == 5
    assert marble.place(7) == 7
    assert marble.place(8) == 1

def test_1():
    players = 9
    last_marble = 25
    marble = Marble(players, last_marble)
    _, score = marble.play()
    assert score == 32

def test_2():
    players = 10
    last_marble = 1618
    marble = Marble(players, last_marble)
    _, score = marble.play()
    assert score == 8317

def test_3():
    players = 13
    last_marble = 7999
    marble = Marble(players, last_marble)
    _, score = marble.play()
    assert score == 146373

def test_4():
    players = 17
    last_marble = 1104
    marble = Marble(players, last_marble)
    _, score = marble.play()
    assert score == 2764

def test_5():
    players = 21
    last_marble = 6111
    marble = Marble(players, last_marble)
    _, score = marble.play()
    assert score == 54718

def test_6():
    players = 30
    last_marble = 5807
    marble = Marble(players, last_marble)
    _, score = marble.play()
    assert score == 37305

def test_part1():
    players = 418
    last_marble = 71339
    marble = Marble(players, last_marble)
    _, score = marble.play()
    assert score == 412127

# def test_part2():
#     players = 418
#     last_marble = 7133900
#     marble = Marble(players, last_marble)
#     _, score = marble.play()
#     assert score == 412127
