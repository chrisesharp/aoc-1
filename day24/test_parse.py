from war import Battle, Group, Damage, fight_battle

input = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""

def test_1():
    battle = Battle(input)
    immune = battle.immune_groups()
    infection = battle.infection_groups()
    assert len(immune) == 2 and len(infection) == 2

def test_2():
    battle = Battle(input)
    groups = battle.immune_groups()
    assert isinstance(groups[1], Group)

def test_3():
    battle = Battle(input)
    immunes = battle.immune_groups()
    infections = battle.infection_groups()
    assert immunes[0].effective_power() == 76619
    assert immunes[1].effective_power() == 24725
    assert infections[0].effective_power() == 92916
    assert infections[1].effective_power() == 53820

def test_4():
    battle = Battle(input)
    immunes = battle.immune_groups()
    group = immunes[1]
    assert group.get_weaknesses() == set([Damage.slashing, Damage.bludgeoning])
    assert group.get_immunities() == {Damage.fire}
    assert group.damage_type() is Damage.slashing
    assert group.get_damage() == 25
    assert group.get_hitpoints() == 1274
    assert group.get_initiative() == 3
    assert group.get_units() == 989

def test_5():
    battle = Battle(input)
    expected = [(801, 17), (17, 4485), (4485, 989), (989, 801)]
    order = battle.target_pairs()
    result = []
    for group in order:
        result.append((group.get_units(), group.target.get_units()))
    assert result == expected

def test_6():
    battle = Battle(input)
    attack_order = battle.attack_order()
    expected = [(4485, 989), (989, 801), (17, 4485), (801, 17)]
    result = []
    for group in attack_order:
        result.append((group.get_units(), group.target.get_units()))
    assert result == expected

def test_7():
    battle = Battle(input)
    winner, units = fight_battle(battle)
    assert winner == "Infection"
    assert  units == 5216