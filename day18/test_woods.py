from woods import Woods


def test_1():
    with open("test.txt") as f:
        input = f.read()
    woods = Woods(input)
    woods.parse()
    assert str(woods) == """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""


def test_2():
    with open("test.txt") as f:
        input = f.read()
    woods = Woods(input)
    woods.parse()
    neighbours = woods.get_neighbourhood((1, 1))
    assert neighbours == [
                            (0, 0), (1, 0), (2, 0),
                            (0, 1), (2, 1),
                            (0, 2), (1, 2), (2, 2)
                        ]
    neighbours = woods.get_neighbourhood((0, 0))
    assert neighbours == [
                                    (1, 0),
                            (0, 1), (1, 1)
                        ]
    neighbours = woods.get_neighbourhood((9, 9))
    assert neighbours == [
                            (8, 8), (9, 8),
                            (8, 9)
                        ]


def test_3():
    with open("test.txt") as f:
        input = f.read()
    woods = Woods(input)
    woods.parse()
    woods.evaluate_neighbourhood()
    this_acre = woods.field[(9, 9)]
    print("acre: ", this_acre.trees, this_acre.lumber)
    assert this_acre.trees == 2
    assert this_acre.lumber == 0


def test_4():
    with open("test.txt") as f:
        input = f.read()
    woods = Woods(input)
    woods.parse()
    neighbours = woods.get_neighbourhood((7, 0))
    assert neighbours == [
                            (6, 0),         (8, 0),
                            (6, 1), (7, 1), (8, 1)
                        ]
    woods.tick()
    this_acre = woods.field[(7, 0)]
    assert this_acre.trees == 1
    assert this_acre.lumber == 3


def test_5():
    with open("test.txt") as f:
        input = f.read()
    expected_1 = """.......##.
......|###
.|..|...#.
..|#||...#
..##||.|#|
...#||||..
||...|||..
|||||.||.|
||||||||||
....||..|.
"""
    expected_10 = """.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||
"""
    woods = Woods(input)
    woods.parse()
    woods.tick()
    print(woods)
    print(expected_1)
    assert str(woods) == expected_1
    for i in range(9):
        woods.tick()
        print(woods)
    assert str(woods) == expected_10


def test_6():
    with open("test.txt") as f:
        input = f.read()
    woods = Woods(input)
    woods.parse()
    woods.run(10)
    assert woods.answer == 1147
