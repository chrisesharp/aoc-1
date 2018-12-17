def power_level(x,y,sn):
    rackid = x + 10
    pwr = rackid * y
    pwr = (pwr + sn) * rackid
    result = str(pwr)
    length = len(result)
    hundreds = 0
    if length>=3:
        hundreds = length-3
        result = int(result[hundreds])
    else:
        result = 0
    return result - 5

class Grid:
    def __init__(self, sn):
        self.sn = sn
        self.cells = [[0]*301 for x in range(301)]
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
        
        if size>0:
            for dx in range(size):
                total_pwr += self.pwr_level((x+dx,y))
            for dy in range(1,size):
                total_pwr += self.pwr_level((x,y+dy))
            total_pwr += self.pwr_square((x+1,y+1),size-1)
            
        return total_pwr
    
    def main(self):
        self.powerup()
        for y in range(1,299):
            for x in range(1,299):
                for z in range(1,300-max(x,y)):
                    this_square = self.pwr_square((x,y),z)
                    if this_square > self.max_power:
                        self.max_power = this_square
                        self.max_power_sq = (x,y,z)
        
        print("Max power = ", self.max_power)
        print("square location: ", self.max_power_sq)
        

if __name__ == "__main__":
    grid = Grid(7315)
    #grid = Grid(18)
    grid.main()
                

    
