from behave import given, when, then
from simulation import Simulation
from unit import Unit, Race

@given(u'the starting state')
def step_impl(context):
    context.sim = Simulation(context.text)

@when(u'I parse')
def step_impl(context):
    context.sim.parse()

@when(u'I determine order')
def step_impl(context):
    context.sim.determine_order()

@then(u'I should have a playfield of {cols:d} x {rows:d}')
def step_impl(context, cols, rows):
    assert context.sim.dimensions() == (cols, rows)

@then(u'I should have units at')
def step_impl(context):
    for row in context.table:
        unit_type = row[0]
        x = int(row[1])
        y = int(row[2])
        unit = context.sim.unit_at((x,y))
        assert str(unit) == unit_type

@then(u'I should have walls at')
def step_impl(context):
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        assert context.sim.wall_at((x,y)) is True

@then(u'I should get the following order')
def step_impl(context):
    order = []
    for row in context.table:
        race = Race.goblin if row[0] == "G" else Race.elf
        x = int(row[1])
        y = int(row[2])
        order.append(Unit((x,y),race))
    result = context.sim.turn_order()
    for i in range(len(order)):
        assert result[i] == order[i]

@then(u'I should have space at {x:d},{y:d}')
def step_impl(context, x, y):
    assert context.sim.unit_at((x,y)) is None

@when(u'I identify targets for first unit')
def step_impl(context):
    context.player = context.sim.turn_order()[0]
    context.targets = context.sim.find_targets(context.player)

@when(u'I identify targets for last unit')
def step_impl(context):
    context.player = context.sim.turn_order().pop()
    context.targets = context.sim.find_targets(context.player)

@then(u'I should get the following targets')
def step_impl(context):
    print("context.targets:",context.targets)
    for row in context.table:
        race = Race.goblin if row[0] == "G" else Race.elf
        x = int(row[1])
        y = int(row[2])
        assert Unit((x,y),race) in context.targets

@when(u'I identify ranges for each target')
def step_impl(context):
    context.ranges = context.sim.find_ranges(context.player, context.targets)

@then(u'I should get the following ranges')
def step_impl(context):
    print("context.ranges:",context.ranges)
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        assert (x,y) in context.ranges

@then(u'I should get the following contacts')
def step_impl(context):
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        print(x,y, context.ranges)
        assert (x,y) in context.ranges
    
@then(u'I should get the following reachable ranges')
def step_impl(context):
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        assert (x,y) in context.reachable


@when(u'I calculate the closest')
def step_impl(context):
    context.reachable, _ = context.sim.find_reachable_targets(context.player, context.ranges)
    context.closest = set([x[0] for x in context.reachable])
    print("Context.closest:", context.closest)


@then(u'I should get the following locations')
def step_impl(context):
    expected_closest = set()
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        expected_closest.add((x,y))
    assert expected_closest == context.closest

@when(u'I choose the target from the closest')
def step_impl(context):
    context.chosen_target = context.sim.find_closest_target(context.player, context.closest)

@then(u'I should move to {x:d},{y:d}')
def step_impl(context, x, y):
    print("chosen:",context.chosen_target)
    assert context.chosen_target == (x,y)


@when(u'I hit the chosen target')
def step_impl(context):
    casualty = context.player.hit(context.player.attack(context.sim.get_units_in_contact(context.player)))
    context.sim.kill(casualty)

@then(u'the unit at {x:d},{y:d} should have {hp:d} hitpoints')
def step_impl(context, x, y, hp):
    unit = context.sim.unit_at((x,y))
    print("hits:",unit.hp)
    assert unit.hp == hp

@then(u'the unit at {x:d},{y:d} should be dead')
def step_impl(context, x, y):
    assert not context.sim.unit_at((x,y))

@when(u'I set the unit at {x:d},{y:d} has {hp:d} hitpoints')
def step_impl(context, x, y, hp):
    unit = context.sim.unit_at((x,y))
    unit.hp = hp
    