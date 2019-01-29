from region_type import Region


class Cave:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.erosions = {}

    def geo_index(self, loc):
        x, y = loc
        if (x == 0 and y == 0) or loc == self.target:
            return 0
        elif y == 0:
            return x * 16807
        elif x == 0:
            return y * 48271
        else:
            e1 = self.erosion((x - 1, y))
            e2 = self.erosion((x, y - 1))
            return e1 * e2
    
    def erosion(self, loc):
        if loc in self.erosions.keys():
            return self.erosions[loc]
        idx = self.geo_index(loc)
        self.erosions[loc] = (idx + self.depth) % 20183
        return self.erosions[loc]

    def region(self, loc):
        return Region(self.erosion(loc) % 3)

    def render(self, loc):
        if loc == (0, 0):
            return "M"
        if loc == self.target:
            return "T"

        region = self.region(loc)
        if region == Region.WET:
            return "="
        elif region == Region.ROCKY:
            return "."
        else:
            return "|"
    
    def risk(self):
        risk = 0
        for y in range(self.target[1]+ 1):
            for x in range(self.target[0] + 1):
                risk += self.region((x,y)).value
        return risk


if __name__ == "__main__":
    cave = Cave(11817, (9,751))
    risk = cave.risk()
    print("Risk level = ", risk)