from multiprocessing import Pool
import operator

def power_level(x, y, sn):
    rackid = x + 10
    pwr = rackid * y
    pwr = (pwr + sn) * rackid
    result = str(pwr)
    length = len(result)
    hundreds = 0
    if length>=3:
        hundreds = length - 3
        result = int(result[hundreds])
    else:
        result = 0
    return result - 5

class Grid:
    def __init__(self, sn):
        self.sn = sn
        self.cells = [ [0] * 301 for x in range(301)]
        self.squares = {}
        self.max_power = 0
        self.max_power_sq = (0,0,3)
        
    def powerup(self):
        for y in range(1,301):
            for x in range(1,301):
                self.cells[y][x] = power_level(x,y,self.sn)
    
    def pwr_level(self, cell):
        x,y = cell
        return self.cells[y][x]
    
    def pwr_square(self, cell, size=3):
        total_pwr = 0
        (x,y) = cell
        cache = self.squares.get((cell,size),None)
        if cache:
            return cache
             
        if size>1:
            total =  self.pwr_square((x+1,y+1),size-1)
            total_pwr += total
            total_pwr += sum(self.cells[y][x:(x+size)])
            total_pwr += sum([self.cells[y+i][x] for i in range(1,size)])
        else:
            total_pwr = self.cells[y][x]
        
        self.squares.update({(cell,size):total_pwr})
        return total_pwr
        
    def grid_section(self, cell, size=302):
        x, y = cell
        total = 0
        sq_loc = (0,0)
        sq_size = 0
        for z in range(1,size-max(x,y)):
            tot = self.pwr_square((x,y),z)
            if tot > total:
                total = tot
                sq_loc = cell
                sq_size = z
        return [total, sq_loc, sq_size]
    
    def main(self):
        self.powerup()
        max_power = 0
        max_power_sq = 0
        with Pool(8) as p:
            (max_power, max_power_sq, max_size) = max(p.map(self.grid_section, [(x,y) for y in range(1,301) for x in range(1,301)]))
        print("Max power = ", max_power)
        print("square location: ", max_power_sq)
        print("square size: ", max_size)


if __name__ == "__main__":
    grid = Grid(7315)
    grid.main()

