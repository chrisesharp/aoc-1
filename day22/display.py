from equipment import Equipment
from region_type import Region

class Display:
    def __init__(self, cave):
        self.cave = cave
        self.target = cave.target
        self.region = cave.region

    def display(self, path, cols):
        output = ""
        width =  self.target[0] + cols
        height = self.target[1] + 6
        for y in range(height):
            for x in range(width):
                output += self.render((x, y), path)
            output += "\n"
        return output
    def render(self, loc, path=[]):
        if len(path)>0:
            RST = "\u001B[0m"
            RED = "\u001B[31m"
            GREEN = "\u001B[32m"
        else:
            RST = RED = GREEN = ""

        output = ""
        if loc == (0, 0):
            output += GREEN + "M" + RST
            return output
        elif loc == self.target:
            output += RED + "T" + RST
            return output
        
        equip = self.render_equipment(loc, path)

        region = self.region(loc)
        if region == Region.WET:
            output += equip + "="
        elif region == Region.ROCKY:
            output += equip + "."
        else:
            output += equip + "|"

        return output + RST
    
    def render_equipment(self, loc, path):
        if len(path)>0:
            YELLOW = "\u001B[33m"
            MAGENTA = "\u001B[35m"
            BLUE = "\u001B[34m"
            BLACK = "\u001B[30m"
        else:
            YELLOW = MAGENTA = BLUE = BLACK = ""
        if (loc, Equipment.torch) in path:
            return YELLOW 
        elif (loc, Equipment.rope) in path:
            return MAGENTA
        elif (loc, Equipment.nothing) in path:
            return BLUE
        else:
            return BLACK