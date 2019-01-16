@5
Feature: determine reach
As a unit
I can determine if a space is reachable
So that I can identify paths for targets

Scenario: available spaces
Given the starting state
"""
#######
#E..G.#
#.#.#.#
#######
"""
When I parse
And I calculate the available spaces for 1,1
Then I should get spaces:
|x:d|y:d|
| 2 | 1 |
| 3 | 1 |
| 1 | 2 |
| 3 | 2 |

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
And I calculate if I can reach the targets
Then I should get the following reachable ranges:
|x:d|y:d| reachable |
| 2 | 1 |   True    |
| 4 | 1 |   False   |


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
And I calculate if I can reach the targets
Then I should get the following reachable ranges:
|x:d|y:d| reachable |
| 3 | 1 |   True    |
| 5 | 1 |   False   |
| 2 | 2 |   True    |
| 5 | 2 |   False   |
| 1 | 3 |   True    |
| 3 | 3 |   True    |

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
