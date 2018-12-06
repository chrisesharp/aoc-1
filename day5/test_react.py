import react

def test_1():
    input = "dabAcCaCBAcCcaDA"
    answer = react.react(input)
    assert answer == "dabCBAcaDA"

def test_2():
    input = "AAbbCC"
    answer = react.react(input)
    assert answer == "AAbbCC"

def test_3():
    input = "dabAcCaCBAcCcaDA"
    answer = react.transform(input)
    assert answer == "daDA"
    