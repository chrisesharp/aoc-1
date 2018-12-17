import sys
from PIL import Image, ImageColor

class Sky:
    def __init__(self):
        self.points = {}
        self.left   = 0
        self.right  = 0
        self.top    = 0
        self.bottom = 0
        self.cols = [10,16,28,34]
        self.scale = 1
    
    def add_point(self, line):
        loc = line[self.cols[0]:self.cols[1]].split(',')
        x = int(int(loc[0].strip())*self.scale)
        y = int(int(loc[1].strip())*self.scale)
        self.left = min(self.left,x)
        self.right = max(self.right,x)
        self.top = min(self.top,y)
        self.bottom = max(self.bottom,y)
        velocity = line[self.cols[2]:self.cols[3]].split(',')
        dx = int(velocity[0].strip())
        dy = int(velocity[1].strip())
        points = self.points.get((x,y),[])
        points.append((dx,dy))
        self.points.update({(x,y):points})
    
    def get_point(self, location):
        if self.points.get(location,False):
            return '#'
        return '.'
    
    def tick(self):
        points = list(self.points)
        new_points = {}
        for point in points:
            velocities = self.points.pop(point)
            (x,y) = point
            for (dx,dy) in velocities:
                new_list = new_points.get((x+dx,y+dy),[])
                new_list.append((dx,dy))
                new_points.update({(x+dx,y+dy):new_list})
        self.points = new_points
    
    def width(self):
        return (self.left, self.right)
    
    def height(self):
        return (self.top, self.bottom)
    
    def bounds(self):
        left = right = top = bottom = 0
        for point in self.points:
            (x,y) = point
            left = min(left,x)
            right = max(right,x)
            top = min(top,y)
            bottom = max(bottom,y)
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
    
    def render(self):
        output = "\n"
        for y in range(self.top, self.bottom+1):
            for x in range(self.left, self.right+1):
                output+=self.get_point((x,y))
            output+='\n'
        return output
    
    def draw(self, tick):
        self.bounds()
        width = (self.right - self.left) + 2
        height = (self.bottom - self.top) + 2
        print("width:",width)
        print("height:",height)
        im = Image.new('1', (width,height))
        for y in range(self.top, self.bottom+1):
            for x in range(self.left, self.right+1):
                output=self.get_point((x,y))
                if output=='#':
                    im.putpixel((x-self.left,y-self.top), ImageColor.getcolor('white', '1'))
        file = str(tick) + ".png"
        im.save(file)
    
    def main(self, file):
        self.cols = [10,24,36,42]
        #self.scale = 1/100
        input_file = open(file, "r")
        for line in input_file:
            sky.add_point(line)
        print(self.left,self.right)
        print(self.top,self.bottom)
        tick=0
        while tick<10619:
            sky.tick()
            tick+=1

        print("Drawing ",tick)
        self.draw(tick)            

if __name__ == "__main__":
    sky = Sky()
    sky.main(sys.argv[1])
        