@4
Feature: determine range
As a unit
I can determine range for targets
So that I can identify paths

Scenario: Simple input
Given the starting state
"""
#######
#E.G..#
#######
"""
When I parse
And I determine order
And I identify targets for first unit
And I identify ranges for each target
Then I should get the following ranges:
|x:d|y:d|
| 2 | 1 |
| 4 | 1 |


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
And I identify ranges for each target
Then I should get the following ranges:
|x:d|y:d|
| 3 | 1 |
| 5 | 1 |
| 2 | 2 |
| 5 | 2 |
| 1 | 3 |
| 3 | 3 |
