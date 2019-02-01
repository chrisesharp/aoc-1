from region_type import Region
from caver import Caver
from display import Display


class Cave:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.erosion_levels = {}
        self.geo_indices = {}
    
    def neighbours(self, loc):
        (x, y) = loc
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        return set(filter(lambda loc: loc[0]>=0 and loc[1]>=0, results))

    def geo_index(self, loc):
        x, y = loc
        if loc == self.target:
            return 0
        elif y == 0:
            return x * 16807
        elif x == 0:
            return y * 48271
        else:
            if loc in self.geo_indices.keys():
                return self.geo_indices[loc]
            left = self.erosion((x - 1, y))
            above = self.erosion((x, y - 1))
            self.geo_indices[loc] = left * above
            return self.geo_indices[loc]
    
    def erosion(self, loc):
        if loc in self.erosion_levels.keys():
            return self.erosion_levels[loc]
        idx = self.geo_index(loc)
        self.erosion_levels[loc] = (idx + self.depth) % 20183
        return self.erosion_levels[loc]

    def region(self, loc):
        return Region(self.erosion(loc) % 3)
    
    def risk(self):
        risk = 0
        for y in range(self.target[1]+ 1):
            for x in range(self.target[0] + 1):
                risk += self.region((x,y)).value
        return risk


if __name__ == "__main__":
    #cave = Cave(11817, (9,751))
    cave = Cave(510, (10,10))
    print("Part 1:")
    print("Risk level:", cave.risk())
    print("Part 2:")
    caver = Caver(cave)
    display = Display(cave)

    time, path = caver.find_target()
    print(display.display(path, 30))
    print("Regions crossed:", len(path)-1)
    print("Time: ", time)
    
    print("But a better solution that doesn't match the AoC answer is...")
    time, path = caver.find_target(False)
    print(display.display(path, 30))
    print("Regions cross: ",len(path)-1)
    print("Time: ",time)