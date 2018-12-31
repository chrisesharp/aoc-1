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

def left(caller, direction):
    return Direction((direction + 3) % 4)

def right(caller,direction):
    return Direction((direction + 1) % 4)

def ahead(caller, direction):
    return direction

def turn(caller, direction):
    return caller.turn(direction)
