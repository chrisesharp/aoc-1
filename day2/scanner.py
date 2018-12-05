import sys
from array import array

class Scanner:
    def __init__(self):
        self.w = 26
        self.h = 250;
        self.codes = [[0 for x in range(self.w)] for y in range(self.h)] 
        pass
        
    
    def main(self, filename):
        file = open(filename, "r")
        print(self.checksum(file))
        print(self.common())
    
    def checksum(self, lines):
        accumulator = [0,0]
        y=0
        for line in lines:
            x=0
            for c in line.strip():
                self.codes[y][x]=ord(c)
                x += 1
            y += 1
            scan = scanline(line)
            for i in range(2):
                if (scan[i]):
                    accumulator[i] += 1
            self.w = x
            self.h = y
        return accumulator[0] * accumulator[1]
    
    def common(self):
        for y in range(self.h-1):
            for i in range(y+1, self.h):
                if self.match(self.codes[i],self.codes[y]):
                    return self.common_chars((y,i))

    def match(self, a, b):
        delta = 0
        for i in range(self.w):
            if a[i]!=b[i]:
                delta+=1
            if delta == 2:
                break
        if delta == 1:
            return True
        return False
        
    def diff(self, a, b):
        delta = 0
        for i in range(self.w):
            delta += abs(a[i]-b[i])
        return delta
    
    def common_chars(self, rows):
        (a,b) = rows
        common = ""
        print(self.codes[a])
        print(self.codes[b])
        for i in range(self.w):
            if (self.codes[a][i] == self.codes[b][i]):
                common+=(chr(self.codes[a][i]))
        return common

def scanline(line):
    twos = 0
    threes = 0
    for char in line:
        count = line.count(char)
        if (count == 2):
            twos+=1
        elif (count ==3):
            threes+=1
        line = line.replace(char,'')
    return (twos>0,threes>0)
    
if __name__ == "__main__":
    scan = Scanner()
    scan.main(sys.argv[1])