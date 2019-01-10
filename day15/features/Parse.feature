@1
Feature: parse initial state
As a sim
I can parse input
So that I can create initial state

Scenario: Sample goblin
Given the starting state
"""
####
#.G#
####
"""
When I parse
Then I should have a playfield of 4 x 3
And I should have units at:
| unit|x:d|y:d|
|  G  | 2 | 1 |
And I should have space at 1,1

Scenario: Sample elf
Given the starting state
"""
####
#E.#
####
"""
When I parse
Then I should have a playfield of 4 x 3
And I should have units at:
| unit|x:d|y:d|
|  E  | 1 | 1 |
And I should have space at 2,1
And I should have walls at:
|x:d|y:d|
| 0 | 0 |
| 1 | 0 |
| 2 | 0 |
| 3 | 0 |
| 0 | 1 |
| 3 | 1 |
| 0 | 2 |
| 1 | 2 |
| 2 | 2 |
| 3 | 2 |