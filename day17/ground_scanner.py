from time import sleep
from direction import Direction, next_location, opposite, below, above
from droplet import Drop 
import sys

class Scanner:
    CLR = "\u001B[H" + "\u001B[2J"
    
    def __init__(self, file):
        self.x_min = 500
        self.x_max = 500
        self.y_min = 0
        self.y_max = 0
        self.spring = (499,0)
        self.ground = {}
        self.ground[self.spring] = "+"
        self.tiles = set()
        
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
        self.x_min = min(x,self.x_min)
        self.x_max = max(x,self.x_max)
        start,end = [int(y) for y in y_range]
        for y in range(start, (end + 1)):
            self.ground[(x,y)] = "#"
    
    def calculate_horizontal(self, start, x_range):
        y = int(start)
        self.y_min = min(y,self.y_min)
        self.y_max = max(y,self.y_max)
        start,end = [int(x) for x in x_range]
        for x in range(start, (end + 1)):
            self.ground[(x,y)] = "#"
    
    def dimensions(self):
        x_range = self.x_min, self.x_max
        y_range = self.y_min, self.y_max
        return (x_range, y_range)
    
    def render(self, cursor=None):
        if cursor:
            drop = cursor.loc
        else:
            drop = (500,0)
        output = "\n"
        for y in range(self.y_min, self.y_max+1):
            for x in range(self.x_min-1, self.x_max+2):
                token = self.ground.get((x,y),".")
                if (x,y) == drop:
                    output +=  "\u001B[31m" + token + "\u001B[0m"
                else:
                    output += token
            output += "\n"
        return output
    
    def drip(self, drop):
        start = drop.loc
        dir = drop.dir
        next = next_location(start, dir)
        this_token = self.ground.get(start,".")
        below_token = self.ground.get(below(start),".")
        next_token = self.ground.get(next,".")

        if below_token == ".":
            dir = Direction.DOWN
            next = next_location(start, dir)
            self.ground[next]="|"
            drop.loc=next
            drop.dir=dir
            drop.reflection=False
            return [drop]
        
        if below_token == "~" and next_token == "#":
            if not drop.reflection:
                self.ground[start]="~"
                dir = opposite(dir)
                next = next_location(start, dir)
                drop.loc=next
                drop.dir=dir
                drop.reflection=True
            else:
                next = above(start)
                dir = opposite(dir)
                drop.loc=next
                drop.dir=dir
                drop.reflection=False
            return [drop]
            
        if below_token == "#" and dir == Direction.DOWN :
            self.ground[start]="~"
            dir = Direction.LEFT
            next = next_location(start, dir)
            drop.loc=next
            drop.dir=dir
            return [drop]
        elif below_token == "#" and next_token == "#":
            if not drop.reflection:
                self.ground[start]="~"
                dir = opposite(dir)
                next = next_location(start, dir)
                drop.loc=next
                drop.dir=dir
                drop.reflection=True
            else:
                next = above(start)
                dir = opposite(dir)
                drop.loc=next
                drop.dir=dir
                drop.reflection=False
            return [drop]
        else:
            self.ground[start]="~"
            next = next_location(start, dir)
            drop.loc=next
            drop.dir=dir
            return [drop]
        drop.loc=next
        drop.dir=dir
        return [drop]
        
    
    def main(self, amount):
        print(Scanner.CLR)
        print(self.render())
        droplets = [ Drop(self.spring, Direction.DOWN)]
        while (amount):
            drop = droplets[0]
            droplets = self.drip(drop)
            sleep(1/2)
            print(Scanner.CLR)
            print(self.render(drop))
            print(drop,dir)
            amount -=1

if __name__ == "__main__":
    if len(sys.argv)>1:
        amount = sys.argv[1]
    else:
        amount = 15
    #file = open("input.txt", "r")
    file = open("test1.txt", "r")
    scanner = Scanner(file)
    scanner.main(int(amount))
                