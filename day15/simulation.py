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
        self.FPS = 1/50
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
                    occupier.set_sim(self)
                    self.elves+=1
                if token == "G":
                    self.units.append((x,y))
                    occupier = Unit((x,y),token)
                    occupier.set_sim(self)
                    self.goblins+=1
                if token == "#":
                    self.walls.append((x,y))
                    occupier = token
                self.field[(x,y)] = Cell((x,y),occupier)
    
    def render(self, current=None, lists=[]):
        output = ""
        flat_list = [item for sublist in lists for sublist2 in sublist for item in sublist2]
        output = CLR
        output += "Round: " + str(self.round) + "\tElves:" + str(self.elves) 
        output += ", Goblins:" + str(self.goblins) + "\t" + str(self.count) + "\n" 
        if current:
            output += "Current unit: " + str(current) + "\n"
        for y in range(self.rows):
            hits = []
            for x in range(self.columns):
                if (x,y) in flat_list or (x,y) == current:
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
    
    def summary(self):
        output = ""
        hitpoints = 0
        for loc in self.units:
            hitpoints += self.unit_at(loc).hp
        if self.elves > self.goblins:
            winner = "Elves"
        else:
            winner = "Goblins"
        output += "Combat ends after " + str(self.round) + " full rounds\n"
        output += winner + " win with " + str(hitpoints) + " total hit points left\n"
        output += "Outcome: " + str(self.round) + " * " 
        output += str(hitpoints) + " = " + str(hitpoints * self.round)+"\n"
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
            if not self.is_occupied(loc):
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
            contacts = dict(sorted(contacts.items(), key=lambda x: (x[1].occupier.hp,x[1].loc[1],x[1].loc[0])))
        return contacts
        
    def get_clear_cells(self, target):
        adjacents = set()
        for loc in self.get_adjacents(target.loc):
            if not self.is_occupied(loc):
                adjacents.add(self.field[loc])
        return adjacents
    
    def wall_at(self, loc):
        return loc in self.walls
    
    def determine_order(self):
        self.unit_order = []
        for loc in sorted(self.units, key=lambda x: (x[1],x[0])):
            self.unit_order.append(self.field[loc].occupier)
        return self.unit_order
    
    def turn_order(self):
        return self.unit_order
    
    def get_adjacents(self, loc):
        (target_x, target_y) = loc
        points = (  (target_x, target_y - 1),
                    (target_x - 1, target_y),
                    (target_x, target_y + 1),
                    (target_x + 1, target_y)
                )
        return [loc for loc in points if self.is_reachable(loc)]

    def is_reachable(self, loc):
        x,y = loc
        if (x<0 or x>=self.columns): 
            return False
        if (y<0 or y>=self.rows): 
            return False
        return  True
    
    def is_occupied(self, loc):
        return loc in self.units or loc in self.walls
    
    def kill(self, unit):
        target = unit.loc
        self.units.remove(target)
        self.field[target] = Cell(target)
        if unit.race == "G":
            self.goblins-=1
        else:
            self.elves-=1

    def still_turns_to_play(self, rounds):
        return (rounds - self.round) != 0
    
    def unit_turn(self, unit):
        if not unit.is_alive():
            return True
            
        targets = unit.find_targets(self.turn_order())
        if not targets:
            return False
            
        ranges = unit.find_ranges(targets)
        if not ranges:
            return True
            
        if unit.loc in ranges:
            chosen_target = unit.attack()
            unit.hit(chosen_target)
            return True
        
        #print(self.render(unit.loc,[[ranges]]))
        reachable, closed = unit.find_reachable_targets(ranges)
        if not reachable:
            return True
        #print(self.render(unit.loc,[reachable]))
        min_dist, chosen = unit.choose_closest_target(reachable)
        chosen_target = unit.choose_best_path(min_dist, chosen, closed)
        contacts=None
        if chosen_target:
            self.units.remove(unit.loc)
            self.field[unit.loc] = Cell(unit.loc)
            unit.loc = chosen_target
            self.field[unit.loc] = Cell(unit.loc,unit)
            self.units.append(unit.loc)
            contacts = self.get_contacts(unit)
        if contacts:
            chosen_target = unit.attack()
            unit.hit(chosen_target)
        return True
    
    def move_unit(self, unit, destination):
        self.units.remove(unit.loc)
        self.field[unit.loc] = Cell(unit.loc)
        unit.loc = destination
        self.field[unit.loc] = Cell(unit.loc,unit)
        self.units.append(unit.loc)
        return unit
        
    def combat(self, rounds):
        while self.still_turns_to_play(rounds):
            print(self.render())
            for unit in self.determine_order():
                #print(self.render([[[unit.loc]]]))
                print(self.render())
                if not self.unit_turn(unit):
                    return
            self.round += 1

    def main(self, rounds):
        self.parse()
        self.combat(rounds)
        print(self.render([]))
        hitpoints = 0
        print(self.summary())

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

        