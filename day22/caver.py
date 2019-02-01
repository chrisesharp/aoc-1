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
    
    def search(self):
        search = PriorityQueue()
        search.put(self.start, 0)
        time_so_far = {}
        time_so_far[self.start] = 0
        trail = {}
        trail[self.start] = None

        while not search.empty():
            (current, holding) = search.get_item()
            if self.found_target(current, holding):
                break

            for item in Equipment:
                if item != holding and self.right_equipment(item, current):
                    new_time = time_so_far[(current, holding)] + 7
                    if (current, item) not in time_so_far or new_time < time_so_far[(current, item)]:
                        time_so_far[(current, item)] = new_time
                        search.put( (current, item), new_time + self.heuristic(current))
                        trail[(current, item)] = (current, holding)

            for next in self.cave.neighbours(current):
                if self.right_equipment(holding, next):
                    new_time = time_so_far[(current, holding)] + 1
                    if (next, holding) not in time_so_far or new_time < time_so_far[(next, holding)]:
                        time_so_far[(next, holding)] = new_time
                        search.put((next, holding), new_time + self.heuristic(next))
                        trail[(next, holding)] = (current, holding)
        return time_so_far, trail

    def better_search(self):
        start = self.start
        search = PriorityQueue()
        search.put(start, 0)
        time_so_far = {}
        trail = {}
        time_so_far[start] = 0
        trail[start] = None

        while not search.empty():
            (current, holding) = search.get_item()
            if self.found_target(current, holding):
                break
            
            for next in self.cave.neighbours(current):
                for item in Equipment:
                   if self.right_equipment(item, next):
                        new_time = time_so_far[(current, holding)] + self.cost(holding, item)
                        if (next, item) not in time_so_far or new_time < time_so_far[(next, item)]:
                            time_so_far[(next, item)] = new_time
                            priority = new_time + self.heuristic(next)
                            search.put((next, item), priority)
                            trail[(next, item)] = (current, holding)
        return time_so_far, trail
    
    def follow_trail(self, trail):
        start = self.start
        current = (self.cave.target, Equipment.torch)
        path = []
        while current != start:
            path.append(current)
            current = trail[current]
        path.append(start)
        path.reverse()
        return path

    def find_target(self, official=True):
        if official:
            time_so_far, trail = self.search()
        else:
            time_so_far, trail = self.better_search()
        path = self.follow_trail(trail)
        return time_so_far[(self.cave.target, Equipment.torch)], path