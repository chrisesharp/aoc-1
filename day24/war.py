import re
import sys
from enum import IntEnum


class Damage(IntEnum):
    fire = 0
    cold = 1
    bludgeoning = 2
    slashing = 3
    radiation = 4

class Battle():
    def __init__(self, input, boost=0):
        self.input = input
        self.immune = []
        self.infect = []
        self.immunity_boost = boost
        self.parse()
        self.winner = None
        self.impasse = False
    
    def parse(self):
        immune, infect = re.split("\n\n", self.input)
        immune = re.split("\n",immune)[1:]
        infect = re.split("\n",infect)[1:]
        for group in immune:
            self.immune.append(Group(group, True, self.immunity_boost))
        for group in infect:
            self.infect.append(Group(group, False))
    
    def immune_groups(self):
        return list(self.immune)
    
    def infection_groups(self):
        return list(self.infect)
    
    def find_candidates(self, attacker, defenders):
        candidates = []
        for target in defenders:
            if attacker.damage_type() in target.get_weaknesses():
                candidates.append((target, 2))
            elif attacker.damage_type() not in target.get_immunities():
                candidates.append((target, 1))
        return candidates
    
    def target_pairs(self):
        order = []
        immune_system = list(self.immune)
        infection = list(self.infect)
        targets = sorted(self.immune + self.infect, 
                        key=lambda x: (x.effective_power(), x.get_initiative()),
                        reverse=True )
        for attacker in targets:
            attacker.target = None
            defenders = infection if attacker.is_immune_system else immune_system
            candidates = self.find_candidates(attacker, defenders)
            
            if candidates:
                chosen = None
                dmg_mod = 1
                best_damage = -1
                for target, multiplier in candidates:
                    potential = attacker.effective_power() * multiplier
                    if potential < best_damage:
                        continue
                    if potential > best_damage or \
                        target.effective_power() > chosen.effective_power() or \
                        target.effective_power() == chosen.effective_power() and \
                        target.get_initiative() > chosen.get_initiative():
                        best_damage = potential
                        chosen = target
                        dmg_mod = multiplier
                attacker.target = chosen
                attacker.dmg_mod = dmg_mod
                defenders.remove(chosen)
            order.append(attacker)
        return order

    def attack_order(self):
        combatants = self.target_pairs()
        return sorted(combatants, key=lambda x: x.get_initiative(), reverse=True)

    def fight(self):
        self.impasse = True
        for attacker in self.attack_order():
            if attacker.get_units() > 0 and attacker.target:
                target_hp = attacker.target.get_hitpoints()
                damage = attacker.get_damage() * attacker.get_units()
                casualties = min(attacker.target.get_units(), int(damage / target_hp))
                if casualties:
                    self.impasse = False
                    attacker.target.units = attacker.target.get_units() - casualties
        self.immune = list(filter(lambda x: x.units > 0, self.immune))
        self.infect = list(filter(lambda x: x.units > 0, self.infect))
        if not self.immune:
            self.winner = self.infect
        if not self.infect:
            self.winner = self.immune

class Group():
    immunities = re.compile(r"immune to ")
    weaknesses = re.compile(r"weak to ")
    pattern = re.compile(r"(?P<units>\d+) units each with (?P<hitpoints>\d+) hit points.?(?P<effects>\([^)]*\))? with an attack that does (?P<damage>\d+) (?P<damage_type>\w+) damage at initiative (?P<initiative>\d+)")
    
    def __init__(self, text, is_immune_system, boost=0):
        self.target = None
        self.dmg_mod = 1
        self.is_immune_system = is_immune_system
        self.weaknesses = {}
        self.immunities = {}
        self.props = Group.pattern.match(text).groupdict()
        self.hitpoints = int(self.props["hitpoints"])
        self.damage = int(self.props["damage"]) + boost
        self.units = int(self.props["units"])
        self.initiative = int(self.props["initiative"])
        
        effects = re.split('; ', self.props["effects"][1:-1]) if self.props["effects"] else []
        
        for effect in effects:
            matched = Group.immunities.match(effect)
            if matched:
                self.immunities = find_effect(matched, effect)
            matched = Group.weaknesses.match(effect)
            if matched:
                self.weaknesses = find_effect(matched, effect)
    
    def get_units(self):
        return self.units

    def get_hitpoints(self):
        return self.hitpoints

    def get_immunities(self):
        return self.immunities
    
    def get_weaknesses(self):
        return self.weaknesses
    
    def get_damage(self):
        return self.damage * self.dmg_mod

    def damage_type(self):
        return Damage[self.props["damage_type"]]
    
    def get_initiative(self):
        return self.initiative
    
    def effective_power(self):
        return self.units * self.damage

def find_effect(match, effect):
    effects = []
    for damage_type in re.split(', ', effect[match.end(0):]):
        effects.append(Damage[damage_type])
    return set(effects)

def fight_battle(battle):
    while (not battle.winner and not battle.impasse):
        battle.fight()
    
    total_units = 0
    winner = None
    if battle.winner:
        for group in battle.winner:
            total_units += group.get_units()
            if group.is_immune_system:
                winner = "Immune System"
            else:
                winner = "Infection"
    return winner, total_units

def main(file):
    with open(file, 'r') as myfile:
        input = myfile.read()
    
    print("Part 1:")
    winner, total_units = fight_battle(Battle(input))
    print("Winning army (", winner, ") has: ", total_units)
    print()
    print("Part 2:")
    winner = None
    boost = 0
    while (winner != "Immune System"):
        boost += 1
        winner, total_units = fight_battle(Battle(input, boost))
    print("Winning army (", winner, ") has: ", total_units, " with boost ", boost)


if __name__ == "__main__":
    main(sys.argv[1])