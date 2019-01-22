from enum import IntEnum


class Direction(IntEnum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

def next_location(coords, direction):
    return {
        Direction.LEFT: lambda coords: ((coords[0] - 1),
                                        coords[1]),
        Direction.RIGHT: lambda coords: ((coords[0] + 1),
                                         coords[1]),
        Direction.UP: lambda coords: (coords[0],
                                      (coords[1] - 1)),
        Direction.DOWN: lambda coords: (coords[0],
                                        (coords[1] + 1))
        }[direction](coords)

def below(coords):
    return  ((coords[0], coords[1]+1))

def above(coords):
    return  ((coords[0], coords[1]-1))
    
def opposite(direction):
    return Direction((direction + 2) % 4)
