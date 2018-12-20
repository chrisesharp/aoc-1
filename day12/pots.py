class Pots:
    def __init__(self, initial):
        self.pots =  "....." + initial + "....................."
        self.offset = 5
        self.start = 5
        self.end = len(initial) + self.offset
        self.rules = {}
    
    def add_rules(self, rules):
        self.rules = rules
    
    def read_rules(self, file):
        input = open(file, "r").readlines()
        rules = {}
        for line in input:
            rule = line[:5]
            state = line[9]
            rules.update({rule:state})
        self.add_rules(rules)
    
    def apply_rules(self, width=39):
        next_gen = ["." for x in range(width)]
        for i in range(self.start-3,self.end+6):
            matched = False
            state = ""
            offset = 0
            if i==-2:
                section = ".." + self.pots[:i+5]
            elif i==-1:
                section = "." + self.pots[:i+5]
            elif i==len(self.pots)-2:
                section = self.pots[i:] + ".."
            elif i==len(self.pots)-1:
                section = self.pots[i:] + "."
            else:
                section = self.pots[i:i+5]
            if section in self.rules:
                matched = True
                state = self.rules.get(section)
            if matched:
                next_gen[i+2]= state
        self.pots =  "".join(next_gen)
        return self.pots
    
    def count_plants(self):
        total = 0
        self.start = len(self.pots)
        self.end = 0
        for i in range(len(self.pots)):
            if self.pots[i] == '#':
                self.start = min(self.start,i)
                self.end = max(self.end,i)
                total += i - self.offset
        return total
        
    def count_last(self, iteration):
        self.pots = "###...###...###...###...###...###...###...###...###...###...###...###...###...###...###...###...###...###...###...###...###...###....###...###"
        self.start_pot = 54 + (iteration - 91)
        print("For iteration ",iteration,"\nStart pot = ", self.start_pot)
        print("offset = ", self.offset)
        total = 0
        for i in range(len(self.pots)):
            if self.pots[i] == '#':
                total += i + self.start_pot - self.offset
        return total
    
    def print_gen(self):
        output = ""
        for i in range(self.start-1,self.end+2):
            output += self.pots[i]
        return output
    
    def main(self, width):
        pots.read_rules("input.txt")
        #pots.read_rules("test.txt")
        print("  \t      0         1         2          3")
        print("  \t      |         0         0          0")
        print("0 :\t",self.pots)
        for i in range(1,93):
            self.apply_rules(width)
            plants = self.count_plants()
            row = self.print_gen()
            print(i,":\t",row, self.start,self.end,self.offset, plants)
        print("Offset:", self.offset)
        print("Total plants: ",plants)
        print("Total for 5B: ", self.count_last(50000000000))

if __name__ == "__main__":
    initial = "#.####...##..#....#####.##.......##.#..###.#####.###.##.###.###.#...#...##.#.##.#...#..#.##..##.#.##"
    #initial = "#..#.#..##......###...###"
    pots = Pots(initial)
    pots.main(550)