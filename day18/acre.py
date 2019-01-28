from land import Land


class Acre:
    state_tokens = {
        Land.CLEARING: ".",
        Land.TREES:    "|",
        Land.LUMBER:   "#"
    }

    token_states = {
        ".":    Land.CLEARING,
        "|":    Land.TREES,
        "#":    Land.LUMBER
    }

    def __init__(self, state=Land.CLEARING):
        self.state = state
        self.trees = 0
        self.lumber = 0

    def __str__(self):
        return Acre.state_tokens[self.state]

    def set_tree_neighbours(self, trees):
        self.trees = trees

    def set_lumber_neighbours(self, lumber):
        self.lumber = lumber

    def is_tree(self):
        return self.state == Land.TREES

    def is_lumber(self):
        return self.state == Land.LUMBER

    def grow(self):
        if self.state == Land.CLEARING and self.trees >= 3:
            self.state = Land.TREES
            return

        if self.state == Land.TREES:
            if self.lumber >= 3:
                self.state = Land.LUMBER
            return

        if self.state == Land.LUMBER and self.trees > 0 and self.lumber > 0:
            return

        self.state = Land.CLEARING
        return


def new_acre(token="."):
    return Acre(Acre.token_states[token])
