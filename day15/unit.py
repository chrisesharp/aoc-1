class Unit:
    def __init__(self, loc, race):
        self.loc = loc
        self.race = race
    
    def __str__(self):
        return self.race
    
    def __eq__(self, other):
        if isinstance(other, Unit):
            return self.loc == other.loc and self.race == other.race
        return False
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    
    def find_targets(self, units):
        return list(filter(lambda x: x.race != self.race, units))
    
    def find_ranges(self, targets):
        ranges = []
        for target in targets:
            adjacents = self.sim.get_clear_space(target.loc)
            ranges.extend(adjacents)
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
    
    def find_closest_targets(self, targets):
        available_spaces = self.available_space(self.loc)
        reachable_targets = []
        for target in targets:
            if self.is_reachable(target, available_spaces):
                reachable_targets.append(target)
        targets_distance = {}
        for target in reachable_targets:
            print("finding path for ", target)
            path = self.sim.find_path(self.loc,target)
            if path:
                targets_distance[target]=path
                print("found one of length ",len(targets_distance[target]))
        
        min_path_length = 99
        shortest = {}
        for path in (sorted(targets_distance.items(), key=lambda x: len(x[1]) )):
            if len(path[1]) <= min_path_length:
                min_path_length = len(path[1])
                shortest[path[0]]=path[1]
            else:
                break
        return shortest
    
    def choose_target(self, targets):
        if targets:
            return list(sorted(targets.keys(), key=lambda x: (x[1],x[0])))[0]
        return None
    