from graph import Graph

def test_1():
    input = ["Step A must be finished before step C can begin."]
    graph = Graph()
    graph.parse(input)
    assert graph.get_avail()[0] == "A"

def test_2():
    input = ["Step C must be finished before step A can begin.",
             "Step C must be finished before step F can begin."]
    graph = Graph()
    graph.parse(input)
    assert graph.get_avail()[0] == "C"

def test_3():
    input = open("test.txt", "r")
    graph = Graph()
    graph.parse(input)
    assert graph.get_avail()[0] == "C"

def test_4():
    input = open("test.txt", "r")
    graph = Graph()
    graph.parse(input)
    path = graph.find_ordered_path()
    assert path == list('CABDFE')

def test_5():
    input = open("test.txt", "r")
    graph = Graph()
    graph.parse(input)
    path,time = graph.find_with_workers(2)
    assert path == list('CABFDE')
    assert time == 15