@7
Feature: fight target
As a unit
I can hit a target
So that I can reduce their hitpoints and kill them

Scenario: elf hits goblin
Given the starting state
"""
#####
#EG.#
#####
"""
When I parse
And I determine order
And I identify targets for first unit
And I identify ranges for each target
And I calculate the closest
And I choose the target from the closest
And I hit the chosen target
Then the unit at 2, 1 should have 197 hitpoints

Scenario: goblin hits elf
Given the starting state
"""
#####
#EG.#
#####
"""
When I parse
And I determine order
And I identify targets for last unit
And I identify ranges for each target
And I calculate the closest
And I choose the target from the closest
And I hit the chosen target
Then the unit at 1, 1 should have 197 hitpoints

Scenario: elf hits right goblin
Given the starting state
"""
#######
#EG...#
#G..#.#
#...#.#
#######
"""
When I parse
And I set the unit at 2, 1 has 3 hitpoints
And I set the unit at 1, 2 has 3 hitpoints
And I determine order
And I identify targets for first unit
And I identify ranges for each target
And I calculate the closest
And I choose the target from the closest
And I hit the chosen target
Then the unit at 1, 2 should have 3 hitpoints
Then the unit at 2, 1 should be dead

Scenario: elf hits weaker goblin
Given the starting state
"""
#######
#EG...#
#G..#.#
#...#.#
#######
"""
When I parse
And I set the unit at 2, 1 has 5 hitpoints
And I set the unit at 1, 2 has 3 hitpoints
And I determine order
And I identify targets for first unit
And I identify ranges for each target
And I calculate the closest
And I choose the target from the closest
And I hit the chosen target
Then the unit at 2, 1 should have 5 hitpoints
And the unit at 1, 2 should be dead

