from caves import Cave
from region_type import Region

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
    output = ""
    width =  cave.target[0] + 6
    height = cave.target[1] + 6
    for y in range(height):
        for x in range(width):
            output += cave.render((x, y))
        output += "\n"
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
