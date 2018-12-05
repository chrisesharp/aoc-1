import sys

class Claim:
    def __init__(self):
        self.locations = {}
        self.claims = {}
    
    def main(self, filename):
        file = open(filename, "r")
        self.parse(file)
        overlap = self.calculate()
        print(overlap)
        
    def area(self, key):
        input = self.claims.get(key)
        this_area = set()
        parts = input.split(':')
        orig = parts[0].split(',')
        dims = parts[1].split('x')
        origX = int(orig[0])
        origY = int(orig[1])
        width = int(dims[0])
        height = int(dims[1])
        for y in range(origY, origY + height):
            for x in range(origX, origX + width):
                this_area.add((x,y))
                list = self.locations.get((x,y))
                if (list is None):
                    list = [key]
                else:
                    list.append(key)
                self.locations.update({(x,y):list})
        return this_area
    
    def parse(self, input):
        for line in input:
            parts = line.split('@')
            self.claims.update({parts[0].strip():parts[1].strip()})
    
    def calculate(self):
        for claim in self.claims:
            self.area(claim)
        overlap = 0
        overlapping = set()
        unique = ""
        for loc in self.locations:
            usage = len(self.locations.get(loc))
            if usage>=2:
                overlap+=1
                for claim in self.locations.get(loc):
                    overlapping.add(claim)
        unique = (set(self.claims).difference(overlapping))
        return (overlap, unique)

if __name__ == "__main__":
    claim = Claim()
    claim.main(sys.argv[1])