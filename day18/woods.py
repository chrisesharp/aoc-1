from acre import new_acre
import sys

CLR = "\u001B[H" + "\u001B[2J"


class Woods:
    def __init__(self, input):
        self.input = input.split("\n")
        cols = len(self.input[0])
        rows = len(self.input)
        self.locs = [(x, y) for y in range(rows) for x in range(cols)]
        self.rows = rows
        self.cols = cols
        self.trees = 0
        self.lumber = 0
        self.field = {}

    def parse(self):
        for (x, y) in self.locs:
            token = self.input[y][x]
            self.field[(x, y)] = new_acre(token)

    def render(self):
        output = ""
        for y in range(self.rows):
            for x in range(self.cols):
                acre = self.field[(x, y)]
                output += str(acre)
            output += "\n"
        return output

    def __str__(self):
        return self.render()

    def get_neighbourhood(self, loc):
        neighbours = []
        x, y = loc
        deltas = [
            (x-1, y-1), (x, y-1),   (x+1, y-1),
            (x-1, y),               (x+1, y),
            (x-1, y+1), (x, y+1),   (x+1, y+1),
        ]
        for (dx, dy) in deltas:
            if dx >= 0 and dx < self.cols and \
                    dy >= 0 and dy < self.rows:
                neighbours.append((dx, dy))
        return neighbours

    def evaluate_neighbourhood(self):
        for loc in self.locs:
            this_acre = self.field[loc]
            trees = 0
            lumber = 0
            for neighbour_loc in self.get_neighbourhood(loc):
                acre = self.field[neighbour_loc]
                if acre.is_tree():
                    trees += 1
                elif acre.is_lumber():
                    lumber += 1
            this_acre.set_tree_neighbours(trees)
            this_acre.set_lumber_neighbours(lumber)

    def new_crop(self):
        new_field = {}
        self.trees = 0
        self.lumber = 0
        for loc in self.locs:
            this_acre = self.field[loc]
            this_acre.grow()
            if this_acre.is_tree():
                self.trees += 1
            elif this_acre.is_lumber():
                self.lumber += 1
            new_field[loc] = this_acre
        return new_field

    def tick(self):
        self.evaluate_neighbourhood()
        self.field = self.new_crop()

    def run(self, iterations):
        already_seen = {}
        prev_cycle = 0

        i = 0
        while i < iterations:
            self.tick()
            i += 1
            print(CLR)
            print(self)
            resources = self.trees * self.lumber
            cycle = i - already_seen.get(resources, 0)
            if cycle == prev_cycle:
                if iterations % cycle == i % cycle:
                    self.answer = resources
                    break
            already_seen[resources] = i
            prev_cycle = cycle
            print(i, resources)
            self.answer = resources


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        input = f.read()
    woods = Woods(input)
    woods.parse()
    print("Part1:")
    woods.run(10)
    print("Answer: ", woods.answer)
    print("Part2:")
    woods.parse()
    woods.run(1000000000)
    print("Answer: ", woods.answer)
