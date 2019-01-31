from caves import Cave, Caver
from region_type import Region

RST = "\u001B[0m"
RED = "\u001B[31m"
GREEN = "\u001B[32m"
YELLOW = "\u001B[33m"
MAGENTA = "\u001B[35m"
BLUE = "\u001B[34m"
BLACK = "\u001B[30m"

def test_1():
    cave = Cave(510, (10,10))
    loc = (0, 0)
    idx = cave.geo_index(loc)
    assert idx == 0
    assert cave.erosion(loc) == 510
    assert cave.region(loc) == Region.ROCKY

def test_2():
    cave = Cave(510, (10,10))
    loc = (0, 1)
    idx = cave.geo_index(loc)
    assert idx == 48271
    assert cave.erosion(loc) == 8415
    assert cave.region(loc) == Region.ROCKY

def test_3():
    cave = Cave(510, (10,10))
    loc = (1, 0)
    idx = cave.geo_index(loc)
    assert idx == 16807
    assert cave.erosion(loc) == 17317
    assert cave.region(loc) == Region.WET

def test_4():
    cave = Cave(510, (10,10))
    loc = (10, 10)
    idx = cave.geo_index(loc)
    assert idx == 0
    assert cave.erosion(loc) == 510
    assert cave.region(loc) == Region.ROCKY

def test_5():
    cave = Cave(510, (10,10))
    loc = (1, 1)
    idx = cave.geo_index(loc)
    assert idx == 145722555
    assert cave.erosion(loc) == 1805
    assert cave.region(loc) == Region.NARROW

def test_6():
    cave = Cave(510, (10,10))
    output = cave.display([], 6)
    print(output)
    assert "\n" + output == """
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||
"""

def test_7():
    cave = Cave(510, (10,10))
    assert cave.risk() == 114

def test_8():
    cave = Cave(510, (1,1))
    neighbours = cave.neighbours((1, 1))
    assert neighbours == {(1, 0), (0, 1), (2, 1), (1, 2) }

def test_8a():
    cave = Cave(510, (1,1))
    neighbours = cave.neighbours((0, 1))
    assert neighbours == {(0, 0), (0, 2), (1, 1) }

def test_8b():
    cave = Cave(510, (1,1))
    neighbours = cave.neighbours((0, 0))
    assert neighbours == {(1, 0), (0, 1) }

def test_8c():
    cave = Cave(510, (1,1))
    neighbours = cave.neighbours((1, 0))
    assert neighbours == {(0, 0), (1, 1), (2, 0) }

def test_9():
    cave = Cave(510, (1,0))
    caver = Caver(cave)
    time, _ = caver.find_target()
    assert time == 1

def test_10():
    cave = Cave(510, (10,10))
    caver = Caver(cave)
    time, _ = caver.find_target()
    assert time == 45

def test_11():
    cave = Cave(11817, (9,751))
    cave.scanner((90,1500)) 
    assert cave.region((89, 1499)) == Region.WET

def test_12():
    cave = Cave(510, (10,10))
    caver = Caver(cave)
    _, came_from = caver.search()
    path = caver.reconstruct_path(came_from)
    received = cave.display(path, 6)
    print(received)
    received = received.replace(RST, "")
    received = received.replace(RED, "")
    received = received.replace(GREEN, "")
    received = received.replace(BLUE, "")
    received = received.replace(MAGENTA, "")
    received = received.replace(BLACK, "")
    received = received.replace(YELLOW, "")
    assert "\n" + received == """
M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||
"""