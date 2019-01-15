from unit import Unit
from cell import Cell
import sys
from time import sleep
import heapq

ESC = "\u001B["
CLR = "\u001B[H" + "\u001B[2J"
RST = "\u001B[0m"
REVON = "\u001B[?5h"
REVOFF = "\u001B[?5l"
BLINK = "\u001B[5m"
REV = "\u001B[7m"

class Simulation:
    def __init__(self, input):
        self.input = input
        self.units = []
        self.elves = 0
        self.goblins = 0
        self.walls = []
        self.field = {}
        self.unit_order = None
        self.round = 0
        self.current_unit = None
        self.FPS = 1/30
        self.count = 0
        
    
    def parse(self):
        self.columns = self.input.index("\n")
        input_rows = self.input.split('\n')
        self.rows = len(input_rows)
        
        for y in range(self.rows):
            for x in range(self.columns):
                token = input_rows[y][x]
                occupier = None
                if token == "E":
                    self.units.append((x,y))
                    occupier = Unit((x,y),token)
                    self.elves+=1
                if token == "G":
                    self.units.append((x,y))
                    occupier = Unit((x,y),token)
                    self.goblins+=1
                if token == "#":
                    self.walls.append((x,y))
                    occupier = token
                self.field[(x,y)] = Cell((x,y),occupier)
    
    def render(self, lists=[]):
        output = ""
        flat_list = [item for sublist in lists for sublist2 in sublist for item in sublist2]
        output = CLR
        output += "Round: " + str(self.round) + "\tCurrent Unit: " + str(self.current_unit) + "\t" + str(self.count) + "\n" 
        for y in range(self.rows):
            hits = []
            for x in range(self.columns):
                if (x,y) in flat_list:
                    output += ESC + "31m" + "*" + RST
                else:
                    output += str(self.field[(x, y)])
                if (x,y) in self.units:
                    unit = self.unit_at((x,y))
                    hits.append(str(unit.race)+"("+str(unit.hp)+")")
            output += "\t\t" + " ".join(hits) + "\n"
        sleep(self.FPS)
        self.count+=1
        return output
    
    def dimensions(self):
        return (self.columns, self.rows)
    
    def unit_at(self, loc):
        if loc in self.units:
            return self.field.get(loc).occupier
        return None
    
    def get_clear_space(self, target):
        adjacents = set()
        for loc in self.get_adjacents(target):
            if loc not in self.units and loc not in self.walls:
                adjacents.add(loc)
        return adjacents
    
    def get_contacts(self, unit):
        contacts = None
        for loc in self.get_adjacents(unit.loc):
            if loc in self.units:
                adjacent =  self.field.get(loc)
                if adjacent.occupier.race != unit.race:
                    if not contacts: contacts = {}
                    contacts[loc]=adjacent
        
        if contacts:
            contacts = dict(sorted(contacts.items(), key=lambda x: x[1].occupier.hp))
        return contacts
        
    def get_clear_cells(self, target):
        adjacents = set()
        for loc in self.get_adjacents(target.loc):
            if loc not in self.units and loc not in self.walls:
                adjacents.add(self.field[loc])
        return adjacents
        
    
    def wall_at(self, loc):
        return loc in self.walls
    
    def determine_order(self):
        self.unit_order = []
        for loc in sorted(self.units, key=lambda x: (x[1],x[0])):
            self.unit_order.append(self.field[loc].occupier)
    
    def turn_order(self):
        return self.unit_order
    
    def get_adjacents(self, loc):
        target_x = loc[0]
        target_y = loc[1]
        return  [
                (target_x, max(0, target_y-1)),
                (max(0, target_x-1), target_y),
                (min(self.columns-1, target_x+1), target_y),
                (target_x, min(self.rows-1, target_y+1))                
                ]


    def find_path(self, start, target, weights):
        start = self.field[start]
        target = self.field[target]
        opened = []
        heapq.heapify(opened)
        closed = set()

        heapq.heappush(opened, (start.f, start))
        while len(opened):
            (f, cell) = heapq.heappop(opened)
            closed.add(cell)

            if cell is target:
                return self.path_of(cell, start)
            
            for adj_cell in self.get_clear_cells(cell):
                if adj_cell not in closed:
                    if (adj_cell.f, adj_cell) in opened:
                        if adj_cell.g >= cell.g + 10:
                            self.update_cell(adj_cell, cell, target, weights)
                    else:
                        self.update_cell(adj_cell, cell, target, weights)
                        heapq.heappush(opened, (adj_cell.f, adj_cell))

    def find_paths(self, start, target):
        paths = []
        for weight in [(1,1),(1,2),(2,1)]:
            paths.append(self.find_path(start, target, weight))
        return paths
            
    def path_of(self, cell, start):
        path = []
        path.append(cell.loc)
        while cell.parent is not start:
            cell = cell.parent
            path.append(cell.loc)
        path.reverse()
        return path
    
    def get_heuristic(self, cell, target, weights):
        (a,b) = weights
        return 10 * ((abs(cell[0] - target[0])*a) + (abs(cell[1] - target[1])*b))
    
    def update_cell(self, adj, cell, target, weights):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj.loc, target.loc, weights)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def combat(self, rounds):
        while (rounds - self.round) != 0:
            print(self.render([]))
            self.determine_order()
            units = self.turn_order()
            for unit in units:
                self.current_unit = unit.loc
                unit.set_sim(self)
                targets = unit.find_targets(units)
                if not targets:
                    return
                ranges, contacts = unit.find_ranges(targets)
                #print(self.render([[[self.current_unit]]]))
                if not contacts:
                    closest = unit.find_closest_targets(ranges)
                    chosen_target = unit.choose_target(closest)
                    #print(self.render([closest.values()]))
                    if chosen_target:
                        self.units.remove(self.current_unit)
                        self.field[self.current_unit] = Cell(self.current_unit)
                        unit.loc = closest[chosen_target][0]
                        self.field[unit.loc] = Cell(unit.loc,unit)
                        self.units.append(unit.loc)
                        contacts = self.get_contacts(unit)
                if contacts:
                    chosen_target = unit.choose_target(contacts)
                    unit.hit(chosen_target)
            #if self.winner:
            #    return
            self.round += 1
    
    def main(self, rounds):
        self.parse()
        self.winner = False
        self.combat(rounds)
        print(self.render([]))
        hitpoints = 0
        for loc in self.units:
            hitpoints += self.unit_at(loc).hp
        if self.elves > self.goblins:
            winner = "Elves"
        else:
            winner = "Goblins"
        print("Combat ends after ",self.round," full rounds")
        print(winner," win with ", hitpoints, "total hit points left")
        print("Outcome: ", self.round, " * ", hitpoints," = ", hitpoints * self.round)
    

if __name__ == "__main__":
    file = sys.argv[1]
    if len(sys.argv)>2:
        max_rounds = int(sys.argv[2])
    else:
        max_rounds = -1
    with open(file, 'r') as myfile:
        input = myfile.read()
    sim = Simulation(input)
    sim.main(max_rounds)

        