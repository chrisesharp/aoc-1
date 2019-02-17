import sys
from linked_list import Node

class Scoreboard:
    def __init__(self, target):
        self.recipes = [3,7]
        self.elf = [0,1]
        self.target = target
    
    def new_recipes(self):
        new = str(self.recipes[self.elf[0]] + self.recipes[self.elf[1]])
        return list(map(lambda x: int(x), new))
        
    def iterate(self, target):
        while len(self.recipes) < (target+10):
            self.recipes+=(self.new_recipes())
            self.choose_recipes()
    
    def scores(self):
        return self.recipes
    
    def choose_recipes(self):
        elf1 = self.recipes[self.elf[0]]
        elf2 = self.recipes[self.elf[1]]
        self.elf[0] = (1 + self.elf[0] + elf1) % len(self.recipes)
        self.elf[1] = (1 + self.elf[1] + elf2) % len(self.recipes)
    
    def stringify(self, num_list):
        return "".join(list(map(lambda x: str(x), num_list)))
    
    def ten_recipes(self):
        return self.stringify(self.recipes[self.target:self.target+10])
    
    def scan(self, target, chunksize):
        found_target = None
        count = chunksize
        while not found_target:
            self.iterate(count)
            recipes = self.stringify(self.recipes)
            index = recipes.find(target)
            if index > -1:
                found_target = index
                break
            count+=chunksize
        return found_target
    
    def main(self):
        self.iterate(self.target)
        print(self.ten_recipes())
    
    def main_pt2(self):
        print(self.scan(str(self.target),21000000))

if __name__ == "__main__":
    input = 681901
    score = Scoreboard(input)
    print("Part 1:")
    score.main()
    print("Part 2:")
    score.main_pt2()
    