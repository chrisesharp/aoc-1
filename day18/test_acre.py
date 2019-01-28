from acre import Acre
from land import Land


def test_1():
    acre = Acre()
    acre.set_tree_neighbours(0)
    acre.set_lumber_neighbours(0)
    acre.grow()
    assert str(acre) == "."


def test_2():
    acre = Acre()
    acre.set_tree_neighbours(3)
    acre.set_lumber_neighbours(0)
    acre.grow()
    assert str(acre) == "|"


def test_3():
    acre = Acre()
    acre.set_tree_neighbours(1)
    acre.set_lumber_neighbours(3)
    acre.grow()
    assert str(acre) == "."


def test_4():
    acre = Acre(Land.TREES)
    acre.set_tree_neighbours(1)
    acre.set_lumber_neighbours(3)
    acre.grow()
    assert str(acre) == "#"


def test_5():
    acre = Acre(Land.LUMBER)
    acre.set_tree_neighbours(1)
    acre.set_lumber_neighbours(3)
    acre.grow()
    assert str(acre) == "#"


def test_6():
    acre = Acre(Land.LUMBER)
    acre.set_tree_neighbours(0)
    acre.set_lumber_neighbours(3)
    acre.grow()
    assert str(acre) == "."
