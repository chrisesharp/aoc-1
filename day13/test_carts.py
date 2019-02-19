from direction import Direction
from track import Track
 
def test_1():
    with open("test1.txt") as f:
        input = f.read()
    track = Track(input)
    track.parse()
    carts = track.get_carts()
    assert carts[0].get_location() == (0,1)
    assert carts[0].get_direction() == Direction.DOWN
    assert carts[1].get_location() == (0,5)
    assert carts[1].get_direction() == Direction.UP

def test_2():
    with open("test1.txt") as f:
        input = f.read()
    track = Track(input)
    track.parse()
    track.tick()
    carts = track.get_carts()
    assert carts[0].get_location() == (0,2)
    assert carts[1].get_location() == (0,4)

def test_3():
    with open("test1.txt") as f:
        input = f.read()
    track = Track(input)
    track.parse()
    while not track.get_crash():
        track.tick()
    assert track.get_crash() == (0,3)

def test_4():
    with open("test4.txt") as f:
        input = f.read()
    track = Track(input)
    track.parse()

    while not track.get_crash():
        track.tick()
    assert track.get_crash() == (7,3)

def test_5():
    with open("test4.txt") as f:
        input = f.read()
    with open("test4_out.txt") as f:
        expected = f.read()
    track = Track(input)
    track.parse()
    output = ""
    while not track.get_crash():
        output += track.tick()
    output = output.rstrip("\n")
    print(output)
    assert track.get_crash() == (7,3)
    assert output == expected

def test_6():
    with open("test6.txt") as f:
        input = f.read()
    with open("test6_out.txt") as f:
        expected = f.read()
    track = Track(input)
    track.parse()
    output = ""
    while len(track.carts)>1:
        output += track.tick()
    output = output.rstrip("\n")
    print(output)
    assert output == expected

def test_7():
    with open("input.txt") as f:
        input = f.read()
    track1 = Track(input, False)
    track1.parse()
    track1.run_sim(None, True)
    assert track1.get_crash() == (45, 34)
    
    track2 = Track(input, False)
    track2.parse()
    track2.run_sim(None, False)
    assert track2.carts[0].get_location() == (91, 25)
    