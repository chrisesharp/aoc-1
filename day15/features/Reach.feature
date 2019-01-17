@5
Feature: determine reach
As a unit
I can determine if a space is reachable
So that I can identify paths for targets

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
And I calculate the closest
Then I should get the following locations:
|x:d|y:d|
| 2 | 1 |


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
And I calculate the closest
Then I should get the following locations:
|x:d|y:d|
| 3 | 1 |
| 2 | 2 |
| 1 | 3 |

Scenario: finding closest
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
Then I should get the following locations:
|x:d|y:d|
| 2 | 2 |
| 3 | 1 |
| 1 | 3 |

Scenario: contacts in reach
Given the starting state
"""
#######
#EG.G.#
#...#.#
#.G.#G#
#######
"""
When I parse
And I determine order
And I identify targets for first unit
And I identify ranges for each target
And I calculate the closest
Then I should get the following locations:
|x:d|y:d|
| 1 | 1 |
