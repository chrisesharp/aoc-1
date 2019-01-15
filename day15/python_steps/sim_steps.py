from behave import given, when, then
from simulation import Simulation
from unit import Unit

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
        assert unit.race == unit_type

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
        race = row[0]
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
    units = context.sim.turn_order()
    context.player = units[0]
    context.player.set_sim(context.sim)
    context.targets = context.player.find_targets(units)

@when(u'I identify targets for last unit')
def step_impl(context):
    units = context.sim.turn_order()
    context.player = units.pop()
    context.player.set_sim(context.sim)
    context.targets = context.player.find_targets(units)

@then(u'I should get the following targets')
def step_impl(context):
    for row in context.table:
        race = row[0]
        x = int(row[1])
        y = int(row[2])
        assert Unit((x,y),race) in context.targets

@when(u'I identify ranges for each target')
def step_impl(context):
    context.ranges, context.contacts = context.player.find_ranges(context.targets)

@then(u'I should get the following ranges')
def step_impl(context):
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        assert (x,y) in context.ranges

@then(u'I should get the following contacts')
def step_impl(context):
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        print(x,y, context.contacts)
        assert (x,y) in context.contacts
        
@when(u'I calculate if I can reach the targets')
def step_impl(context):
    context.reachable = {}
    for target in context.ranges:
        context.reachable[target]=context.player.is_reachable(target)
    
@then(u'I should get the following reachable ranges')
def step_impl(context):
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        reachable = row[2]
        assert str(context.reachable[(x,y)]) == str(reachable)

@when(u'I calculate the available spaces for {x:d},{y:d}')
def step_impl(context, x, y):
    unit = context.sim.unit_at((x,y))
    unit.set_sim(context.sim)
    context.available_spaces = unit.available_space((x,y))

@then(u'I should get spaces')
def step_impl(context):
    expected_spaces = set()
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        expected_spaces.add((x,y))
    print("expcted:", expected_spaces)
    print("avail:", context.available_spaces )
    assert expected_spaces == context.available_spaces


@when(u'I calculate the closest')
def step_impl(context):
    if context.contacts:
        print("contacts:",context.contacts)
        context.closest = context.contacts
    else:
        context.closest = context.player.find_closest_targets(context.ranges)
    print("Context.closest:", context.closest)


@then(u'I should get the following locations')
def step_impl(context):
    expected_closest = set()
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        expected_closest.add((x,y))
    assert expected_closest == context.closest.keys()

@when(u'I choose the target from the closest')
def step_impl(context):
    context.chosen_target = context.player.choose_target(context.closest)

@then(u'I should choose {x1:d},{y1:d} and move to {x2:d},{y2:d}')
def step_impl(context, x1, y1, x2, y2):
    print("chosen:",context.chosen_target)
    assert context.chosen_target == (x1,y1)
    assert context.closest[context.chosen_target][0] == (x2,y2)


@when(u'I hit the chosen target')
def step_impl(context):
    context.player.hit(context.chosen_target)


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
    