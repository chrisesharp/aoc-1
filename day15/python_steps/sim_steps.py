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
    context.first_unit = units[0]
    context.first_unit.set_sim(context.sim)
    context.targets = context.first_unit.find_targets(units[1:])

@then(u'I should get the following targets')
def step_impl(context):
    for row in context.table:
        race = row[0]
        x = int(row[1])
        y = int(row[2])
        assert Unit((x,y),race) in context.targets

@when(u'I identify ranges for each target')
def step_impl(context):
    context.ranges = context.first_unit.find_ranges(context.targets, context.sim)

@then(u'I should get the following ranges')
def step_impl(context):
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        assert (x,y) in context.ranges

@when(u'I calculate if I can reach the targets')
def step_impl(context):
    context.reachable = {}
    for target in context.ranges:
        context.reachable[target]=context.first_unit.is_reachable(target)
    
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
    context.closest = context.first_unit.find_closest_targets(context.ranges)


@then(u'I should get the following locations')
def step_impl(context):
    expected_closest = set()
    for row in context.table:
        x = int(row[0])
        y = int(row[1])
        expected_closest.add((x,y))
    assert expected_closest == context.closest.keys()