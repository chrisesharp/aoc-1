from cell import Cell

class Unit:
    def __init__(self, loc, race):
        self.loc = loc
        self.race = race
        self.atk = 3
        self.hp = 200
    
    def __str__(self):
        return self.race
    
    def __eq__(self, other):
        if isinstance(other, Unit):
            return self.loc == other.loc and self.race == other.race
        return False
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    
    def find_targets(self, units):
        targets = list(filter(lambda x: x.race != self.race, units))
        if not targets:
            self.sim.winner = True
        return targets
    
    def find_ranges(self, targets):
        contacts = self.sim.get_contacts(self)
        
        ranges = []
        for target in targets:
            adjacents = self.sim.get_clear_space(target.loc)
            ranges.extend(adjacents)
        return ranges, contacts
    
    def set_sim(self, sim):
        self.sim = sim
    
        
    def is_reachable(self, target, available=None):
        if not available:
            available = self.available_space(self.loc)
        return (target in available)
    
    def available_space(self, loc, spaces=set()):
        options = self.sim.get_clear_space(loc)
        if not options:
            return spaces
        if options.issubset(spaces):
            return spaces
        
        spaces = spaces.union(options)
        for option in options:
            new_spaces = self.available_space(option, spaces)
            if new_spaces:
                spaces = spaces.union(new_spaces)
        return spaces
    
    def find_closest_targets(self, targets):
        available_spaces = self.available_space(self.loc)
        reachable_targets = []
        for target in targets:
            if self.is_reachable(target, available_spaces):
                reachable_targets.append(target)
        targets_distance = {}
        for target in sorted(reachable_targets, key=lambda x: (x[1],x[0])):
            targets_distance[target] = self.sim.find_paths(self.loc, target)

        min_path_length = 99
        shortest = {}
        for (target, paths) in targets_distance.items():
            min_target_path_length = 99
            for path in sorted(paths, key=lambda x: len(x)):
                if len(path) <= min_path_length:
                    min_path_length = len(path)
                    if len(path) < min_target_path_length:
                        min_target_path_length = len(path)
                        shortest[target]=path
                    elif len(path) == min_target_path_length:
                        existing = shortest[target][0]
                        this = path[0]
                        if (this[1],this[0]) < (existing[1],existing[0]):
                            shortest[target]=path
                    else:
                        break

        shortest2={}
        for path in (sorted(shortest.items(), key=lambda x: len(x[1]) )):
            if len(path[1]) <= min_path_length:
                min_path_length = len(path[1])
                shortest2[path[0]]=path[1]
            else:
                break

        return shortest2
    
    def choose_target(self, targets):
        if targets:
            return list(targets.keys())[0]
        return None
    
    def hit(self, target):
        opponent = self.sim.unit_at(target)
        opponent.hp -= self.atk
        if opponent.hp <= 0:
            self.sim.units.remove(target)
            self.sim.field[target] = Cell(target)
            if opponent.race == "G":
                self.sim.goblins-=1
                if self.sim.goblins==0:
                    self.sim.winner=True
            else:
                self.sim.elves-=1
                if self.sim.elves==0:
                    self.sim.winner=True

    