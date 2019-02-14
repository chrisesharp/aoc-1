import re
import sys
from enum import IntEnum


class Damage(IntEnum):
    fire = 0
    cold = 1
    bludgeoning = 2
    slashing = 3
    radiation = 4

class War():
    def __init__(self, input):
        self.input = input
        self.immune = None
        self.infect = None
        self.parse()
        self.winner = None
    
    def __iter__(self):
        self.combatants = list(sorted(self.immune, key=lambda x: (x.effective_power(), x.get_initiative())))
        self.combatants.extend(list(sorted(self.infect, key=lambda x: (x.effective_power(), x.get_initiative()))))
        return self
    
    def __next__(self):
        if len(self.combatants) is not 0:
            return self.combatants.pop()
        else:
            raise StopIteration
    
    def parse(self):
        immune, infect = re.split("\n\n", self.input)
        immune = re.split("\n",immune)[1:]
        infect = re.split("\n",infect)[1:]
        groups = []
        for group in immune:
            groups.append(Group(group, True))
        self.immune = groups
        groups = []
        for group in infect:
            groups.append(Group(group, False))
        self.infect = groups
    
    def immune_groups(self):
        return list(self.immune)
    
    def infection_groups(self):
        return list(self.infect)
    
    def target_pairs(self):
        order = []
        immune_system = list(self.immune)
        infection = list(self.infect)
        target_selection = iter(self)
        for attacker in target_selection:
            attacker.target = None
            # print("Selecting for ", attacker)
            candidates = []
            if attacker.is_immune_system:
                defenders = infection
            else:
                defenders = immune_system
            
            for target in defenders:
                if attacker.damage_type() in target.get_weaknesses():
                    candidates.append((target, 2))
                elif attacker.damage_type() not in target.get_immunities():
                    candidates.append((target, 1))
            
            if len(candidates) > 0:
                chosen = None
                dmg_mod = 1
                best_damage = -1
                for target, multiplier in candidates:
                    potential = attacker.effective_power() * multiplier
                    if potential > best_damage:
                        best_damage = potential
                        chosen = target
                        dmg_mod = multiplier
                    elif potential == best_damage:
                        if target.effective_power() > chosen.effective_power():
                            chosen = target
                            dmg_mod = multiplier
                        elif target.effective_power() == chosen.effective_power():
                            if target.get_initiative() > chosen.get_initiative():
                                chosen = target
                                dmg_mod = multiplier
                attacker.target = chosen
                attacker.dmg_mod = dmg_mod
                defenders.remove(chosen)
                # print("Chosen ", str(chosen), " removed from ", print_groups(defenders))
            order.append(attacker)
        return order

    def attack_order(self, combatants):
        return sorted(combatants, key=lambda x: x.get_initiative(), reverse=True)

    def fight(self):
        target_order = self.target_pairs()
        # print("Target order:", print_groups(target_order))
        attack_order = self.attack_order(target_order)
        # print("Attack order:", print_groups(attack_order))
        for attacker in attack_order:
            if attacker.get_units() > 0 and attacker.target:
                # print("Attacker: ", attacker.get_units(), ", defender: ", attacker.target.get_units())
                target_hp = attacker.target.get_hitpoints()
                damage = attacker.get_damage() * attacker.get_units()
                casualties = min(attacker.target.get_units(), int(damage / target_hp))
                # print("Casualties: ", casualties)
                attacker.target.units = attacker.target.get_units() - casualties
        self.immune = list(filter(lambda x: x.units > 0, self.immune))
        if len(self.immune) == 0:
            self.winner = self.infect
        self.infect = list(filter(lambda x: x.units > 0, self.infect))
        if len(self.infect) == 0:
            self.winner = self.immune

class Group():
    def __init__(self, text, is_immune_system):
        immunities = re.compile(r"immune to ")
        weaknesses = re.compile(r"weak to ")
        self.is_immune_system = is_immune_system
        self.weaknesses = {}
        self.immunities = {}
        self.props = re.match(r"(?P<units>\d+) units each with (?P<hitpoints>\d+) hit points.?(?P<effects>\([^)]*\))? with an attack that does (?P<damage>\d+) (?P<damage_type>\w+) damage at initiative (?P<initiative>\d+)", text).groupdict()
        self.hitpoints = int(self.props["hitpoints"])
        self.damage = int(self.props["damage"])
        self.units = int(self.props["units"])
        self.initiative = int(self.props["initiative"])
        self.target = None
        self.dmg_mod = 1
        effects = self.props["effects"]
        if effects:
            effects = effects[1:].rstrip(")")
        else:
            effects = ""
        
        for effect in re.split('; ', effects):
            match = immunities.match(effect)
            if match:
                self.immunities = find_effect(match, effect)
            match = weaknesses.match(effect)
            if match:
                self.weaknesses = find_effect(match, effect)
    
    def __str__(self):
        output = "units: " + str(self.units) + ", EP:" + str(self.effective_power()) + ", Init: " + str(self.initiative)
        return output
    
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
    if match:
        immunities = []
        types = re.split(', ', effect[match.end(0):])
        for damage_type in types:
            immunities.append(Damage[damage_type])
        return set(immunities)
    return None

def print_groups(groups):
    output = "["
    for group in groups:
        output += "(" + str(group) + ")"
    output += "]"
    return output

def main(file):
    with open(file, 'r') as myfile:
        input = myfile.read()
    war = War(input)
    while (not war.winner):
        # print("==========")
        war.fight()
        # print("Immune System:")
        # for group in  war.immune_groups():
            # print(group)
        # print("Infection:")
        # for group in  war.infection_groups():
            # print(group)
    print("+++++++++++++++++")
    total_units = 0
    for group in war.winner:
        print("unit:", group.get_units())
        total_units += group.get_units()
        if group.is_immune_system:
            winner = "(Immune System)"
        else:
            winner = "(Infection)"
    print("Winning army ", winner, " has: ", total_units)

if __name__ == "__main__":
    main(sys.argv[1])