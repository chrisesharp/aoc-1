from unit import Unit
from random import randint

class Simulation:
    def __init__(self, input):
        self.input = input
        self.units = []
        self.walls = []
        self.field = {}
        self.unit_order = None
    
    def parse(self):
        self.columns = self.input.index("\n")
        input_rows = self.input.split('\n')
        self.rows = len(input_rows)
        
        for y in range(self.rows):
            for x in range(self.columns):
                token = input_rows[y][x]
                if token == "G" or token == "E":
                    self.units.append((x,y))
                    self.field[(x,y)] = Unit((x,y),token)
                if token == "#":
                    self.walls.append((x,y))
                    self.field[(x,y)] = token
    
    def dimensions(self):
        return (self.columns, self.rows)
    
    def unit_at(self, loc):
        if loc in self.units:
            return self.field.get(loc)
        return None
    
    def get_clear_space(self, target):
        adjacents = set()
        for loc in self.get_adjacents(target):
            if loc not in self.units and loc not in self.walls:
                adjacents.add(loc)
        return adjacents
    
    def wall_at(self, loc):
        return loc in self.walls
    
    def determine_order(self):
        self.unit_order = []
        for loc in sorted(self.units, key=lambda x: (x[1],x[0])):
            self.unit_order.append(self.field[loc])
    
    def turn_order(self):
        return self.unit_order
    
    def get_adjacents(self, loc):
        target_x = loc[0]
        target_y = loc[1]
        return  [
                (target_x, max(0, target_y-1)),
                (target_x, min(self.rows-1, target_y+1)),
                (max(0, target_x-1), target_y),
                (min(self.columns-1, target_x+1), target_y)
                ]
    
    def find_path(self, start, end, path=[]):
        path = path + [start]
        if start==end:
            return path[1:]
        
        options =  self.get_clear_space(start)
        if len(options) == 0:
            return None
        
        best_path = None
        for next_step in options:
            if next_step not in path:
                new_path = self.find_path(next_step, end, path)
                if new_path:
                    if not best_path or len(new_path) < len(best_path):
                        best_path = new_path
        return best_path
        