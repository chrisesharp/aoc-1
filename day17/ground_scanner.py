from time import sleep
from direction import Direction, next_location, below, above
from droplet import Drop


class Scanner:
    CLR = "\u001B[H" + "\u001B[2J"

    def __init__(self, file):
        self.x_min = 500
        self.x_max = 500
        self.y_min = 99
        self.y_max = 0
        self.spring = (500, 0)
        self.ground = {}
        self.ground[self.spring] = "+"
        self.FPS = 1/30
        self.count = 0
        self.animate = False
        self.lips = []

        for line in file:
            parts = line.split(",")
            origin = parts[0].split("=")
            range = parts[1].split("=")[1].split("..")

            if origin[0] == "x":
                self.calculate_vertical(origin[1], range)
            else:
                self.calculate_horizontal(origin[1], range)

    def calculate_vertical(self, start, y_range):
        x = int(start)
        self.x_min = min(x, self.x_min)
        self.x_max = max(x, self.x_max)
        start, end = [int(y) for y in y_range]
        self.y_min = min(start, self.y_min)
        self.y_max = max(end, self.y_max)
        for y in range(start, (end + 1)):
            self.ground[(x, y)] = "#"

    def calculate_horizontal(self, start, x_range):
        y = int(start)
        self.y_min = min(y, self.y_min)
        self.y_max = max(y, self.y_max)
        start, end = [int(x) for x in x_range]
        self.x_min = min(start, self.x_min)
        self.x_max = max(end, self.x_max)
        for x in range(start, (end + 1)):
            self.ground[(x, y)] = "#"

    def dimensions(self):
        x_range = self.x_min, self.x_max
        y_range = self.y_min, self.y_max
        return (x_range, y_range)

    def render_window(self, drop):
        output = str(self.count) + "\n"
        orig_x, orig_y = drop.loc

        for y in range(orig_y-15, orig_y+15):
            for x in range(orig_x-15, orig_x+15):
                token = self.ground.get((x, y), ".")
                if token in ["~", "|"]:
                    output += "\u001B[34m" + token + "\u001B[0m"
                else:
                    output += token
            output += "\n"
        output += str(drop.loc) + \
            "," + str(drop.dir) + \
            "," + str(drop.origin) + \
            "," + str(drop.reflection) + "\n"
        return output

    def render(self, drops={}):
        output = "\n"
        for y in range(0, self.y_max+1):
            line = ""
            for x in range(self.x_min-1, self.x_max+2):
                token = self.ground.get((x, y), ".")
                if drops.get((x, y), False) and self.debug:
                    line += "\u001B[34m" + token + "\u001B[0m"
                else:
                    line += token
            print(line)
            output += line + "\n"
        return output

    def drip(self, drop):
        start = drop.loc
        dir = drop.dir
        next = next_location(start, dir)
        above_token = self.ground.get(above(start), ".")
        below_token = self.ground.get(below(start), ".")
        next_token = self.ground.get(next, ".")
        this_token = self.ground.get(start, ".")

        if drop.off_map(self.dimensions()):
            return []

        if this_token == "|" and below_token == "|" and dir == Direction.DOWN:
            return []

        if drop.returned():
            drop.up()
            drop1 = Drop(drop.loc, Direction.LEFT)
            drop2 = Drop(drop.loc, Direction.RIGHT)
            return [drop1, drop2]

        if above_token == "~" and \
                next_token == "~" and \
                this_token == "~" and \
                below_token == "~" and dir == Direction.DOWN:
            drop.up()
            drop.dir = Direction.LEFT
            return [drop]

        if below_token == "." or below_token == "|":
            if this_token != "+":
                self.ground[drop.loc] = "|"
            drop.down()
            self.ground[drop.loc] = "|"
            return [drop]

        if below_token == "#" and dir == Direction.DOWN:
            self.ground[start] = str(drop)
            drop1 = Drop(start, Direction.LEFT)
            drop2 = Drop(start, Direction.RIGHT)
            return [drop1, drop2]

        if below_token == "~" and dir == Direction.DOWN:
            drop.down()
            drop1 = Drop(drop.loc, Direction.LEFT)
            drop2 = Drop(drop.loc, Direction.RIGHT)
            return [drop1, drop2]

        if (below_token == "~" or below_token == "#") and next_token == "#":
            self.ground[start] = str(drop)
            lip = next_location(above(start), drop.dir)
            token = self.ground.get(lip, ".")
            if token != "#":
                self.lips.append(lip)
                drop.reflect(lip)
            else:
                drop.reflect()
            return [drop]

        self.ground[start] = str(drop)
        drop.next()
        return [drop]

    def fix_flowing(self):
        for lip in self.lips:
            start_x, start_y = lip
            left = self.ground.get(next_location(lip, Direction.LEFT), "")
            right = self.ground.get(next_location(lip, Direction.RIGHT), "")
            if left == "|":
                self.scan(lip, Direction.RIGHT)
            elif right == "|":
                self.scan(lip, Direction.LEFT)

    def scan(self, loc, direction):
        self.ground[loc] = "|"
        next = next_location(loc, direction)
        token = self.ground.get(next, None)
        while token == "~":
            self.ground[next] = "|"
            next = next_location(next, direction)
            token = self.ground.get(next, None)

    def in_bounds(self, y):
        return y <= self.y_max and y >= self.y_min

    def count_water(self, tile_type):
        print("Size of ground items: ", len(self.ground))
        print("within ", self.y_min, self.y_max)
        tiles = {}
        non_clay = filter(lambda x: x[1] in tile_type, self.ground.items())
        not_zero = filter(lambda x: self.in_bounds(x[0][1]), non_clay)
        for item in [x[0] for x in not_zero]:
            tiles[item] = True
        return tiles

    def main(self, debug, animate):
        self.debug = debug
        self.animate = animate
        print(Scanner.CLR)
        droplets = {Drop(self.spring, Direction.DOWN)}
        while (droplets):
            new_droplets = set()
            for drop in droplets:
                drips = self.drip(drop)
                for drip in drips:
                    new_droplets.add(drip)

            droplets = set(new_droplets)
            if self.animate:
                sleep(self.FPS)
                print(Scanner.CLR)
                if droplets:
                    drops = sorted(enumerate(droplets), key=lambda x: x[1].loc)
                    first_drop = list(drops)[0][1]
                    print(self.render_window(first_drop))
        self.fix_flowing()
        print("Calculating water (Part1):")
        water = self.count_water(["~", "|"])
        print("Map:")
        self.render(water)
        print("Tiles with water: ", len(water))
        print("Calculating resting water (Part 2):")
        water = self.count_water(["~"])
        print("Tiles with resting water: ", len(water))


if __name__ == "__main__":
    file = open("input.txt", "r")
    # file = open("test1.txt", "r")
    scanner = Scanner(file)
    scanner.main(True, False)
