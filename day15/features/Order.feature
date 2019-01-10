@2
Feature: determine turn order
As a sim
I can determine unit order
So that I can adhere to the rules

Scenario: Sample input
Given the starting state
"""
#######
#.G.E.#
#E.G.E#
#.G.E.#
#######
"""
When I parse
And I determine order
Then I should get the following order:
| unit|x:d|y:d|
|  G  | 2 | 1 |
|  E  | 4 | 1 |
|  E  | 1 | 2 |
|  G  | 3 | 2 |
|  E  | 5 | 2 |
|  G  | 2 | 3 |
|  E  | 4 | 3 |