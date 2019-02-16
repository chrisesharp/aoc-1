class Cell:
    def __init__(self, loc, occupier=None):
        self.occupier = occupier
        self.loc = loc
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __str__(self):
        if self.occupier:
            return str(self.occupier)
        return " "
    
    def __lt__(self, other):
        return self.f < other.f
