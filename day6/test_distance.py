from manhattan import distance, bounds, Map

def test_1():
    A = (0,0)
    B = (1,1)
    assert distance(A,B) == 2

def test_2():
    A = (0,0)
    B = (2,1)
    assert distance(A,B) == 3

def test_3():
    A = (0,0)
    B = (255,255)
    assert distance(A,B) == 510
    
def test_4():
    A = (0,200)
    B = (200,200)
    assert distance(A,B) == 200

def test_5():
    points = [(0,0),(255,12),(5,300)]
    assert bounds(points) == [(0,0),(255,300)]

def test_6():
    points = [  (1, 1),
                (1, 6),
                (8, 3),
                (3, 4),
                (5, 5),
                (8, 9)  ]
    map = Map()
    map.parse(points)
    assert (map.minX,map.minY) == (1,1)
    assert (map.maxX,map.maxY) == (8,9)

def test_7():
    points = [  (1, 1),
                (1, 6),
                (8, 3),
                (3, 4),
                (5, 5),
                (8, 9)  ]
    map = Map()
    map.parse(points)
    (x,y) = map.find_largest_point()
    assert (x,y) == (5,5)
    assert map.owners.get((4,5))==(5,5)
    assert map.owners.get((1,4))==None
    assert map.area((5,5)) == 17
    assert map.region_size() == 16
    
    
    