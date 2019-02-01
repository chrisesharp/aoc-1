import sys
import heapq
    
def main(file):
    input = open(file, "r")
    points = []
    for line in input:
        end_point = line.index('>')
        point = line[5:end_point]
        radius = line[end_point+5:]
        (x, y, z) = map(int, point.strip().split(','))
        r = int(radius)
        points.append((x, y, z, r))
    print("Part 1:")
    bot, total = find_bot(points)
    print("Largest range nanobot at ", bot)
    print("Number within range: ", total)
    answer = find_space(points)
    print("Part 2:")
    print("Coordinate nearest most nanobots is ", answer)

def find_space(bots):
    q = []
    for x,y,z,radius in bots:
        distance = abs(x) + abs(y) + abs(z)
        start_of_range = distance - radius
        end_of_range = distance + radius + 1
        heapq.heappush(q, (max(0, start_of_range), 1))
        heapq.heappush(q, (end_of_range, -1))

    count = 0
    maxCount = 0
    result = 0
    while q:
        (distance, end) = heapq.heappop(q)
        count += end
        if count > maxCount:
            result = distance
            maxCount = count
    return result

def find_bot(points):
    largest= max(points, key=lambda x: x[3])
    (x,y,z,_) = largest
    within = []
    for point in points:
        if in_range(largest, point):
            within.append(point)
    return (x,y,z), len(within)

def distance(A,B):
    (x1, y1, z1) = A
    (x2, y2, z2) = B
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

def bounds(points):
    minX = minY = minZ = minR = 999999999
    maxX = maxY = maxZ = maxR =  0
    for point in points:
        (x,y,z,r) = point
        minX=min(x,minX)
        minY=min(y,minY)
        minZ=min(z,minZ)
        maxX=max(x,maxX)
        maxY=max(y,maxY)
        maxZ=max(z,minZ)
        minR=min(r,minR)
        maxR=max(r,maxR)
    return [(minX,minY,minZ,minR),(maxX,maxY,maxZ,maxR)]

def in_range(A,B):
    (x1, y1, z1, r) = A
    (x2, y2, z2, _) = B
    return distance((x1,y1,z1),(x2,y2,z2)) <= r

if __name__ == "__main__":
    main(sys.argv[1])
    