@3
Feature: determine targets
As a unit
I can determine targets
So that I can identify paths

Scenario: Sample input
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
Then I should get the following targets:
|race |x:d|y:d|
|  G  | 4 | 1 |
|  G  | 2 | 3 |
|  G  | 5 | 3 |
