from region_type import Region
from queue import PriorityQueue
from equipment import Equipment

class Caver:
    def __init__(self, cave):
        self.cave = cave
        self.costs = {}
        self.start = ((0,0), Equipment.torch)

    def heuristic(self, step):
        (x1, y1) = self.cave.target
        (x2, y2) = step
        return abs(x1 - x2) + abs(y1 - y2)

    def right_equipment(self, item, loc):
        return item != self.cave.region(loc)

    def cost(self, holding, item):
        if item == holding:
            return 1
        else:
            return 8
 
    def found_target(self, current, equipment):
        return current == self.cave.target and equipment == Equipment.torch
    
    def another_search(self):
        search = PriorityQueue()
        search.put(self.start, 0)
        best = {}
        trail = {}
        trail[self.start] = None
        while not search.empty():
            minutes, option = search.get()
            (current, holding) = option
            if option in best and best[option] <= minutes:
                continue
            best[option] = minutes
            if option == (self.cave.target, Equipment.torch):
                break
            if self.found_target(current, holding):
                break
                
            for item in Equipment:
                if item != holding and self.right_equipment(item, current):
                    search.put( (current, item), minutes + 7 )

            for next in self.cave.neighbours(current):
                if not self.right_equipment(holding, next):
                    continue
                search.put((next, holding), minutes + 1)
        return minutes, trail


    def search(self):
        start = self.start
        search = PriorityQueue()
        search.put(start, 0)
        time_so_far = {}
        trail = {}
        time_so_far[start] = 0
        trail[start] = None

        while not search.empty():
            (minutes, (current, holding)) = search.get()

            if self.found_target(current, holding):
                break
            
            for item in Equipment:
                if item != holding and self.right_equipment(item, current):
                    time_so_far[(current, item)] = minutes + 7
                    search.put( (current, item), minutes + 7 )
            
            for next in self.cave.neighbours(current):
                #for item in Equipment:
                #    if self.right_equipment(item, next):
                if not self.right_equipment(holding, next):
                    continue
                new_time = time_so_far[(current, holding)] + 1
                if (next, item) not in time_so_far or new_time < time_so_far[(next, item)]:
                    time_so_far[(next, item)] = new_time
                    priority = new_time + self.heuristic(next)
                    search.put((next, item), priority)
                    trail[(next, item)] = (current, holding)
        return time_so_far, trail
    
    def reconstruct_path(self, trail):
        start = self.start
        current = (self.cave.target, Equipment.torch)
        path = []
        while current != start:
            path.append(current)
            current = trail[current]
        path.append(start)
        path.reverse()
        return path

    def find_target(self):
        time_so_far, trail = self.another_search()
        # time_so_far, trail = self.search()
        # print(time_so_far)
        return time_so_far, trail
        #path = self.reconstruct_path(trail)
        #return time_so_far[(self.cave.target, Equipment.torch)], path


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

    def render(self, loc, path=[]):
        if len(path)>0:
            RST = "\u001B[0m"
            RED = "\u001B[31m"
            GREEN = "\u001B[32m"
        else:
            RST = RED = GREEN = ""

        output = ""
        if loc == (0, 0):
            output += GREEN + "M" + RST
            return output
        elif loc == self.target:
            output += RED + "T" + RST
            return output
        
        equip = self.render_equipment(loc, path)

        region = self.region(loc)
        if region == Region.WET:
            output += equip + "="
        elif region == Region.ROCKY:
            output += equip + "."
        else:
            output += equip + "|"

        return output + RST
    
    def render_equipment(self, loc, path):
        if len(path)>0:
            YELLOW = "\u001B[33m"
            MAGENTA = "\u001B[35m"
            BLUE = "\u001B[34m"
            BLACK = "\u001B[30m"
        else:
            YELLOW = MAGENTA = BLUE = BLACK = ""
        if (loc, Equipment.torch) in path:
            return YELLOW 
        elif (loc, Equipment.rope) in path:
            return MAGENTA
        elif (loc, Equipment.nothing) in path:
            return BLUE
        else:
            return BLACK
    
    def risk(self):
        risk = 0
        for y in range(self.target[1]+ 1):
            for x in range(self.target[0] + 1):
                risk += self.region((x,y)).value
        return risk
    
    def scanner(self, loc):
        x_max, y_max = loc
        for y in range(y_max):
            for x in range(x_max):
                self.geo_index((x,y))
    
    def display(self, path, cols):
        output = ""
        width =  self.target[0] + cols
        height = self.target[1] + 6
        for y in range(height):
            for x in range(width):
                output += self.render((x, y), path)
            output += "\n"
        return output


if __name__ == "__main__":
    cave = Cave(11817, (9,751))
    # cave = Cave(510, (10,10))
    print("Part 1:")
    print("Risk level:", cave.risk())
    print("Part 2:")
    caver = Caver(cave)
    time, path = caver.find_target()
    #print(cave.display(path, 30))
    print("Regions crossed:", len(path)-1)
    print("Time: ", time)