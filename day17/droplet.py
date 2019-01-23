from direction import Direction, next_location, opposite, above


class Drop:
    def __init__(self, loc, dir):
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
        if self.container_lip:
            if self.container_lip[1] == self.loc[1]:
                self.token = "|"

    def down(self):
        self.dir = Direction.DOWN
        self.token = "|"
        self.next()

    def up(self):
        self.loc = above(self.loc)
        self.reflection = 0
        self.origin = self.loc
        self.token = "~"
        if self.container_lip:
            if self.container_lip[1] == self.loc[1] - 1:
                self.token = "|"

    def reflect(self, lip=None):
        if lip:
            self.container_lip = lip
        self.dir = opposite(self.dir)
        self.reflection += 1

    def returned(self):
        return (self.loc == self.origin) and self.reflection > 1

    def off_map(self, dimensions):
        ((min_x, max_x), (min_y, max_y)) = dimensions
        (x, y) = self.loc
        return y < 0 or y > max_y
