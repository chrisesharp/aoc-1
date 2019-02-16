from cell import Cell
from enum import IntEnum

class Race(IntEnum):
    goblin = 0
    elf = 1

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

    def attack(self, group):
        targets = list(group.values())
        return targets[0].occupier
        
    def hit(self, opponent):
        target = opponent.loc
        opponent.hp -= self.atk
        if opponent.hp <= 0:
            return opponent
        return None

    