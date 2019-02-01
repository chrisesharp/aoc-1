from nanobots import distance, find_bot

def test_1():
    A = (0,0,0)
    B = (1,0,0)
    assert distance(A,B) == 1

def test_2():
    A = (0,0,0)
    B = (4,0,0)
    assert distance(A,B) == 4

def test_3():
    A = (0,0,0)
    B = (0,2,0)
    assert distance(A,B) == 2

def test_4():
    A = (0,0,0)
    B = (0,5,0)
    assert distance(A,B) == 5

def test_5():
    A = (0,0,0)
    B = (0,0,3)
    assert distance(A,B) == 3

def test_6():
    A = (0,0,0)
    B = (1,1,1)
    assert distance(A,B) == 3

def test_7():
    A = (0,0,0)
    B = (1,1,2)
    assert distance(A,B) == 4

def test_8():
    A = (0,0,0)
    B = (1,3,1)
    assert distance(A,B) == 5

def test_9():
    points = [
        (0,0,0,4),
        (1,0,0,1),
        (4,0,0,3),
        (0,2,0,1),
        (0,5,0,3),
        (0,0,3,1),
        (1,1,1,1),
        (1,1,2,1),
        (1,3,1,1)
    ]
    largest, within = find_bot(points)
    assert largest == (0,0,0)
    assert within == 7


    
    