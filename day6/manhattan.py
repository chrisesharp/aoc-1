import sys
import collections

class Map:
    def __init__(self):
        self.points = {}
        self.areas = {}
        self.infinites = []
        self.region = []
        self.owners = {}
        self.max_dist = 32
    
    def parse(self,points):
        for point in points:
            self.points.update({point: 0 })
        bound = bounds(points)
        (self.minX,self.minY),(self.maxX,self.maxY) = bound
        
        
    def find_largest_point(self):
        biggest_area = 0
        owning_point = None
        for y in range(self.minY,self.maxY+1):
            for x in range(self.minX, self.maxX+1):
                owner = self.find_owner((x,y))
                if owner:
                    self.owners.update({(x,y):owner})
                    area_count = len(self.areas.get(owner))
                    if area_count > biggest_area and owner not in self.infinites:
                        biggest_area = area_count
                        owning_point = owner
                    self.points.update({owner:area_count})
        print("biggest owner:",owning_point)
        return owning_point
        
    def find_owner(self,target):
        the_owner = None
        owned = []
        min = 999
        total_dist = 0
        for point in self.points:
            dist = distance(point, target)
            if dist < min:
                min = dist
                owned = [point]
            elif dist == min:
                owned.append(point)
            total_dist+=dist
        the_owner = self.found_owner(target,owned)
        self.check_region(target, total_dist)
        return the_owner
    
    def found_owner(self, target, owned):
        the_owner = None
        if len(owned) == 1:
            the_owner = owned[0]
            points = self.areas.get(the_owner)
            if points is None:
                points = []
            points.append(target)
            self.areas.update({the_owner:points})
            if self.at_edge(target):
                self.infinites.append(the_owner)
        return the_owner
    
    def area(self, point):
        return len(self.areas[point])
    
    def at_edge(self, point):
        (x,y) = point
        return (x==self.minX or x==self.maxX or y==self.minY or y==self.maxY)
    
    def region_size(self):
        return len(self.region)
    
    def check_region(self, target, dist):
        if dist < self.max_dist:
            self.region.append(target)
        
    
def main(file):
    input = open(file, "r")
    points = []
    for point in input:
        (x,y) = point.strip().split(',')
        points.append((int(x),int(y)))
    map = Map()
    map.max_dist = 10000
    map.parse(points)
    (x,y) = map.find_largest_point()
    print("largest area: ",map.area((x,y)))
    print("near region: ",map.region_size())
                
    
def distance(A,B):
    (x,y) = A
    (p,q) = B
    return abs(x-p) + abs(y-q)

def bounds(points):
    minX = minY = 1000
    maxX = maxY = 0
    for point in points:
        (x,y) = point
        minX=min(x,minX)
        minY=min(y,minY)
        maxX=max(x,maxX)
        maxY=max(y,maxY)
    return [(minX,minY),(maxX,maxY)]

if __name__ == "__main__":
    main(sys.argv[1])
    