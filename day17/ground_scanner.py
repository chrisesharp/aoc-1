from time import sleep
from direction import Direction, next_location, below, above
from droplet import Drop
import curses

CLR = "\u001B[H" + "\u001B[2J"
BLUE = "\u001B[34m"
COLOUR_ON = BLUE
COLOUR_OFF = "\u001B[0m"


class Scanner:

    def __init__(self, file):
        self.x_min = 500
        self.x_max = 500
        self.y_min = 99
        self.y_max = 0
        self.spring = (500, 0)
        self.ground = {}
        self.ground[self.spring] = "+"
        self.FPS = 0
        self.animate = False
        self.lips = []
        self.parse(file)
        self.window = [self.spring[0] - 50, self.spring[1] - 15]

    def parse(self, file):
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

    def animate_flow(self, screen, droplets):
        if not self.animate:
            return
        if droplets:
            drops = sorted(enumerate(droplets), key=lambda x: x[1].id)
            first_drop = list(drops)[0][1]
            self.render_window(screen, first_drop)
        sleep(self.FPS)

    def render_window(self, screen, drop):
        x, y = drop.loc
        left_buf = int(self.screen_width / 4)
        right_buf = left_buf * 3
        top_buf = int(self.screen_height / 4)
        bottom_buf = top_buf * 2

        if x < (self.window[0] + left_buf):
            self.window[0] -= 1
        elif x > (self.window[0] + right_buf):
            self.window[0] += 1
        if y < (self.window[1] + top_buf):
            self.window[1] -= 1
        elif y > (self.window[1] + bottom_buf):
            self.window[1] += 1

        y_start = self.window[1] - 15
        x_start = self.window[0]

        for y in range(y_start, y_start + self.screen_height):
            for x in range(x_start, x_start + self.screen_width):
                token = self.ground.get((x, y), ".")
                x1 = x - x_start
                y1 = y - y_start
                if token in ["~", "|"]:
                    screen.addch(y1, x1, ord(token), curses.color_pair(1))
                elif token in ["#"]:
                    screen.addch(y1, x1, ord(token), curses.color_pair(2))
                else:
                    screen.addch(y1, x1, ord(token), curses.A_REVERSE)
        screen.refresh()
        return

    def render(self, drops={}):
        output = "\n"
        for y in range(0, self.y_max+1):
            line = ""
            for x in range(self.x_min-1, self.x_max+2):
                token = self.ground.get((x, y), ".")
                if drops.get((x, y), False) and self.debug:
                    line += COLOUR_ON + token + COLOUR_OFF
                else:
                    line += token
            print(line)
            output += line + "\n"
        return output

    def init_screen(self, screen):
        screen.clear()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        self.screen_width = curses.COLS - 1
        self.screen_height = curses.LINES - 1

    def flow(self, screen, droplets):
        self.init_screen(screen)
        while (droplets):
            new_droplets = set()
            for drop in droplets:
                drips = self.drip(drop)
                new_droplets.update(drips)
            droplets = set(new_droplets)
            self.animate_flow(screen, droplets)
        screen.getkey()

    def drip(self, drop):
        surrounding = self.surrounding(drop)
        (this, next, below, up) = surrounding

        if drop.off_map(self.dimensions()) or drop.in_a_stream(this, below):
            return []

        if drop.returned():
            drop.float_up()
            return drop.split()

        if drop.unsupported(below):
            self.damp_ground(drop)
            drop.down()
            self.wet_ground(drop)
            return [drop]

        if drop.falling():
            if drop.submerged(surrounding):
                drop.float_up()
                return [drop]

            if drop.hit_clay(below):
                self.wet_ground(drop)
            else:
                drop.down()
            return drop.split()

        if drop.landed(below):
            self.wet_ground(drop)
            if drop.hit_clay(next):
                self.check_for_lip(drop)
                drop.reflect()
                return [drop]

            drop.next()
            return [drop]

    def damp_ground(self, drop):
        self.ground[drop.loc] = "|"

    def wet_ground(self, drop):
        self.ground[drop.loc] = str(drop)

    def check_for_lip(self, drop):
        lip = next_location(above(drop.loc), drop.dir)
        if not drop.hit_clay(self.ground.get(lip, ".")):
            self.lips.append(lip)
            drop.found_lip(lip)

    def surrounding(self, drop):
        above_token = self.ground.get(above(drop.loc), ".")
        below_token = self.ground.get(below(drop.loc), ".")
        next_token = self.ground.get(next_location(drop.loc, drop.dir), ".")
        this_token = self.ground.get(drop.loc, ".")
        return (this_token, next_token, below_token, above_token)

    def fix_surface(self):
        for lip in self.lips:
            left = self.ground.get(next_location(lip, Direction.LEFT), "")
            right = self.ground.get(next_location(lip, Direction.RIGHT), "")
            if left == "|":
                self.scan_surface(lip, Direction.RIGHT)
            elif right == "|":
                self.scan_surface(lip, Direction.LEFT)

    def scan_surface(self, loc, direction):
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

        droplets = {Drop(below(self.spring), Direction.DOWN)}
        curses.wrapper(self.flow, droplets)

        print("Calculating water (Part1):")
        water = self.count_water(["~", "|"])

        print("Map:")
        self.render(water)
        print("Tiles with water: ", len(water))

        print("Calculating resting water (Part 2):")
        self.fix_surface()
        water = self.count_water(["~"])
        print("Tiles with resting water: ", len(water))


if __name__ == "__main__":
    file = open("input.txt", "r")
    # file = open("test1.txt", "r")
    scanner = Scanner(file)
    scanner.main(True, True)
