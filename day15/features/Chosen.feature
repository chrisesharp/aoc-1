@6
Feature: choose target
As a unit
I can choose a target
So that I can adhere to the ordering rules

Scenario: choosing closest for first
Given the starting state
"""
#######
#E..G.#
#...#.#
#.G.#G#
#######
"""
When I parse
And I determine order
And I identify targets for first unit
And I identify ranges for each target
And I calculate the closest
And I choose the target from the closest
Then I should move to 2,1

Scenario: choosing closest for last
Given the starting state
"""
#########
#......G#
#..#.##.#
#..G....#
#.#####.#
#...E...#
#########
"""
When I parse
And I determine order
And I identify targets for last unit
And I identify ranges for each target
And I calculate the closest
And I choose the target from the closest
Then I should move to 5,5