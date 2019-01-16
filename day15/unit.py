from cell import Cell

class Unit:
    def __init__(self, loc, race):
        self.loc = loc
        self.race = race
        self.atk = 3
        self.hp = 200
    
    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return self.race
    
    def __eq__(self, other):
        if isinstance(other, Unit):
            return self.loc == other.loc and self.race == other.race
        return False
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    
    def find_targets(self, units):
        return [x for x in units if x.is_alive() and x.race != self.race]


    def find_ranges(self, targets):
        ranges = set()
        for target in targets:
            for loc in self.sim.get_adjacents(target.loc):
                if self.loc == loc or not self.sim.is_occupied(loc):
                    ranges.add(loc)
        return ranges

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
    
    def find_reachable_targets(self, targets):
        open = []
        closed = set()
        seen = []
        reachable = []
        shortest_distance = 9999
        
        open.append((self.loc, 0, None))
        while open:
            target, dist, parent = open.pop(0)
            
            if dist > shortest_distance:
                continue
            
            if target in targets:
                reachable.append((target, dist, parent))
                shortest_distance = dist
            
            cell = (target, dist, parent)
            if cell not in closed:
                closed.add(cell)
            
            if target in seen:
                continue
            seen.append(target)
            
            if target != self.loc and self.sim.is_occupied(target):
                continue
            
            for pos in self.sim.get_adjacents(target):
                open.append((pos, dist + 1, target))
        
        return reachable, closed
                
        
    def find_closest_target(self, targets):
        reachable, closed = self.find_reachable_targets(targets)
        if not reachable:
            return None
        
        min_dist, chosen = self.choose_closest_target(reachable)
        return self.choose_best_path(min_dist, chosen, closed)


    def choose_closest_target(self, reachable):
        min_dist = min(x[1] for x in reachable)
        min_reachable = sorted([x[0] for x in reachable if x[1] == min_dist],
                               key=lambda x: (x[1], x[0]))
        return min_dist, min_reachable[0]
    
    def choose_best_path(self, min_dist, chosen, closed):
        parents = [x for x in closed if x[0] == chosen and x[1] == min_dist]
        while min_dist > 1:
            min_dist -= 1
            new_parents = []
            for _, _, p in parents:
                new_parents.extend(x for x in closed
                                   if x[0] == p and x[1] == min_dist)
            parents = new_parents
        return sorted(set(x[0] for x in parents),
                         key=lambda x: (x[1], x[0]))[0]
    
    def attack(self):
        targets = list(self.sim.get_contacts(self).values())
        return targets[0].occupier
        
    def hit(self, opponent):
        target = opponent.loc
        opponent.hp -= self.atk
        if opponent.hp <= 0:
            self.sim.kill(opponent)

    