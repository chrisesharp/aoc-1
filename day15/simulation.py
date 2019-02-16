from unit import Unit, Race
from cell import Cell
from time import sleep
import sys
import curses


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
        self.FPS = 0
        self.count = 0
        self.reboot = False
        self.elf_atk = 3

    def parse(self):
        self.columns = self.input.index("\n")
        input_rows = self.input.split('\n')
        self.rows = len(input_rows)

        for y in range(self.rows):
            for x in range(self.columns):
                token = input_rows[y][x]
                occupier = None
                if token == "E":
                    self.units.append((x, y))
                    occupier = Unit((x, y), token)
                    occupier.atk = self.elf_atk
                    self.elves += 1
                if token == "G":
                    self.units.append((x, y))
                    occupier = Unit((x, y), token)
                    self.goblins += 1
                if token == "#":
                    self.walls.append((x, y))
                    occupier = token
                self.field[(x, y)] = Cell((x, y), occupier)

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
        output += winner + " win with "
        output += str(hitpoints) + " total hit points left\n"
        output += "Outcome: " + str(self.round) + " * "
        output += str(hitpoints) + " = " + str(hitpoints * self.round)+"\n"
        output += "Final attack power: " + str(self.elf_atk) + "\n"
        return output

    def dimensions(self):
        return (self.columns, self.rows)

    def unit_at(self, loc):
        if loc in self.units:
            return self.field.get(loc).occupier
        return None

    def get_units_in_contact(self, unit):
        contacts = None
        for loc in self.get_adjacents(unit.loc):
            if loc in self.units:
                adjacent = self.field.get(loc)
                if adjacent.occupier.race != unit.race:
                    if not contacts:
                        contacts = {}
                    contacts[loc] = adjacent
        if contacts:
            contacts = dict(sorted(contacts.items(),
                key=lambda x: (x[1].occupier.hp, x[1].loc[1], x[1].loc[0])))
        return contacts

    def wall_at(self, loc):
        return loc in self.walls

    def determine_order(self):
        self.unit_order = []
        for loc in sorted(self.units, key=lambda x: (x[1], x[0])):
            self.unit_order.append(self.field[loc].occupier)
        return self.unit_order

    def turn_order(self):
        return self.unit_order

    def get_adjacents(self, loc):
        (target_x, target_y) = loc
        points = (
                    (target_x, target_y - 1),
                    (target_x - 1, target_y),
                    (target_x, target_y + 1),
                    (target_x + 1, target_y)
                )
        return [loc for loc in points if self.is_reachable(loc)]

    def is_reachable(self, loc):
        x, y = loc
        if (x < 0 or x >= self.columns):
            return False
        if (y < 0 or y >= self.rows):
            return False
        return True

    def is_occupied(self, loc):
        return loc in self.units or loc in self.walls

    def kill(self, unit):
        if not unit:
            return
        target = unit.loc
        self.units.remove(target)
        self.field[target] = Cell(target)
        if unit.race == "G":
            self.goblins -= 1
        else:
            self.elves -= 1
            if self.pt2:
                self.elf_atk += 1
                self.reboot = True

    def still_turns_to_play(self, rounds):
        return (rounds - self.round) != 0

    def find_targets(self, unit):
        return [x for x in self.turn_order() if x.is_alive() and x.race != unit.race]

    def find_ranges(self, unit, targets):
        ranges = set()
        for target in targets:
            for loc in self.get_adjacents(target.loc):
                if unit.loc == loc or not self.is_occupied(loc):
                    ranges.add(loc)
        return ranges

    def find_reachable_targets(self, unit, targets):
        open = []
        closed = set()
        seen = []
        reachable = []
        shortest_distance = 9999

        open.append((unit.loc, 0, None))
        while open:
            target, dist, parent = open.pop(0)

            if dist > shortest_distance:
                continue

            if target in targets:
                reachable.append((target, dist))
                shortest_distance = dist

            cell = (target, dist, parent)
            if cell not in closed:
                closed.add(cell)

            if target in seen:
                continue
            seen.append(target)

            if target != unit.loc and self.is_occupied(target):
                continue

            for loc in self.get_adjacents(target):
                open.append((loc, dist + 1, target))
        return reachable, closed

    def choose_best_path(self, closest, paths):
        (min_dist, chosen) = closest
        parents = [x for x in paths if x[0] == chosen and x[1] == min_dist]
        while min_dist > 1:
            min_dist -= 1
            new_parents = []
            for _, _, p in parents:
                new_parents.extend(x for x in paths
                                   if x[0] == p and x[1] == min_dist)
            parents = new_parents
        return sorted(set(x[0] for x in parents), key=lambda x: (x[1], x[0]))[0]

    def find_closest_target(self, unit, targets):
        reachable_targets, paths = self.find_reachable_targets(unit, targets)
        if not reachable_targets:
            return None
        closest = self.choose_closest_target(reachable_targets)
        return self.choose_best_path(closest, paths)

    def choose_closest_target(self, reachable):
        min_dist = min(x[1] for x in reachable)
        min_reachable = sorted([x[0] for x in reachable if x[1] == min_dist],
                               key=lambda x: (x[1], x[0]))
        return (min_dist, min_reachable[0])

    def play_turn(self, screen, unit):
        if not unit.is_alive():
            return True

        targets = self.find_targets(unit)
        if not targets:
            return False
        # self.render(screen, unit.loc,[[targets]])

        ranges = self.find_ranges(unit, targets)
        if not ranges:
            return True

        # self.render(screen, unit.loc,[[ranges]])
        if unit.loc in ranges:
            chosen_target = unit.attack(self.get_units_in_contact(unit))
            casualty = unit.hit(chosen_target)
            if casualty:
                self.kill(casualty)
            return True

        chosen_target = self.find_closest_target(unit, ranges)
        if not chosen_target:
            return True

        contacts = None
        if chosen_target:
            self.units.remove(unit.loc)
            self.field[unit.loc] = Cell(unit.loc)
            unit.loc = chosen_target
            self.field[unit.loc] = Cell(unit.loc, unit)
            self.units.append(unit.loc)
            contacts = self.get_units_in_contact(unit)
        if contacts:
            chosen_target = unit.attack(contacts)
            casualty = unit.hit(chosen_target)
            if casualty:
                self.kill(casualty)
        return True

    def move_unit(self, unit, destination):
        self.units.remove(unit.loc)
        self.field[unit.loc] = Cell(unit.loc)
        unit.loc = destination
        self.field[unit.loc] = Cell(unit.loc, unit)
        self.units.append(unit.loc)
        return unit
    
    def resolve_combat(self, screen, rounds):
        self.init_screen(screen)
        self.reboot = False
        while self.still_turns_to_play(rounds):
            self.render(screen)
            for unit in self.determine_order():
                if not self.play_turn(screen, unit):
                    return False
                if self.reboot:
                    return True
            sleep(self.FPS)            
            self.round += 1

    def reset_battle(self):
        self.units = []
        self.elves = 0
        self.goblins = 0
        self.walls = []
        self.field = {}
        self.round = 0
        self.reboot = False
        self.parse()
    
    def render(self, screen, current=None, lists=[]):
        output = ""
        flat_list = [item for sublist in lists for sublist2 in sublist for item in sublist2]
        output += "Round: " + str(self.round) + "\tElves:" + str(self.elves)
        output += ", Goblins:" + str(self.goblins)
        output += "\t" + str(self.count) + "\n"
        output += "Elf attack power: " + str(self.elf_atk) + "\n"
        if current:
            output += "Current unit: " + str(current) + "\n"
        screen.addstr(0,0, output)
        for y in range(self.rows):
            hits = []
            for x in range(self.columns):
                if (x, y) in flat_list or (x, y) == current:
                    screen.addch(y+1, x, ord("*"), curses.color_pair(5))
                else:
                    token = self.field[(x, y)]
                    colour = 1
                    if isinstance(token.occupier, Unit):
                        if token.occupier.race == "G":
                            colour = 2
                        else:
                            colour = 3
                    screen.addch(y+1, x, ord(str(token)), curses.color_pair(colour))
                if (x, y) in self.units:
                    unit = self.unit_at((x, y))
                    hits.append(str(unit.race)+"("+str(unit.hp)+")")
            output = "\t\t" + " ".join(hits) + "\n"
            screen.addstr(y+1, x, output)
        screen.refresh()
        self.count += 1
        return output
    
    def init_screen(self, screen):
        screen.clear()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.screen_width = curses.COLS - 1
        self.screen_height = curses.LINES - 1

    def main(self, rounds, pt2=False):
        self.pt2 = pt2
        if pt2:
            self.elf_atk = 4
        self.parse()
        while curses.wrapper(self.resolve_combat, rounds):
            self.reset_battle()
            pass
        # print(self.render([]))
        print(self.summary())


if __name__ == "__main__":
    file = sys.argv[1]
    if len(sys.argv) > 2:
        max_rounds = int(sys.argv[2])
    else:
        max_rounds = -1
    with open(file, 'r') as myfile:
        input = myfile.read()
    sim = Simulation(input)
    sim.main(max_rounds, False)
