from direction import Direction, next_location, opposite, above
import time

class Drop:
    def __init__(self, loc, dir):
        self.id = time.time_ns() + hash(loc)
        self.loc = loc
        self.dir = dir
        self.origin = loc
        self.reflection = 0
        self.container_lip = None
        self.token = "~"

    def __str__(self):
        return self.token

    def __eq__(self, other):
        if isinstance(other, Drop):
            return self.loc == other.loc and self.dir == other.dir
        return False

    def __hash__(self):
        return hash((self.loc, self.dir))

    def next(self):
        self.loc = next_location(self.loc, self.dir)

    def down(self):
        self.dir = Direction.DOWN
        self.token = "|"
        self.next()

    def float_up(self):
        self.loc = above(self.loc)
        self.reflection = 0
        self.origin = self.loc
        self.token = "~"
        self.dir = Direction.LEFT
        if self.container_lip:
            if self.container_lip[1] == self.loc[1] - 1:
                self.token = "|"

    def found_lip(self, loc):
        self.container_lip = loc

    def reflect(self):
        self.dir = opposite(self.dir)
        self.reflection += 1

    def returned(self):
        return (self.loc == self.origin) and self.reflection > 1

    def unsupported(self, below_token):
        return below_token == "." or below_token == "|"

    def falling(self):
        return self.dir == Direction.DOWN

    def in_a_stream(self, this, below):
        return self.falling() and this == "|" and below == "|"

    def submerged(self, surrounding):
        (_, next, below, above) = surrounding
        return above == "~" and below == "~" and next == "~"

    def landed(self, below_token):
        return self.hit_clay(below_token) or self.hit_water(below_token)

    def hit_clay(self, token):
        return token == "#"

    def hit_water(self, token):
        return token == "~"

    def off_map(self, dimensions):
        ((min_x, max_x), (min_y, max_y)) = dimensions
        (x, y) = self.loc
        return y < 0 or y > max_y

    def split(self):
        drop1 = Drop(self.loc, Direction.LEFT)
        drop2 = Drop(self.loc, Direction.RIGHT)
        return [drop1, drop2]
