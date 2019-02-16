import sys

def find_constellations(input):
    points = {}
    for line in input.split():
        point = tuple([int(i) for i in line.split(',')])
        assimilated = False
        linked = {}
        for known_point in list(points.keys()):
            if close_enough(known_point, point):
                points, linked = assimilate(point, known_point, points, linked)
                assimilated = True
        
        if not assimilated:
            points[point]=set(point)

        if linked:
            linked_constellations = list(linked.items())
            first_point, constellation = linked_constellations.pop()
            for other_point, other_constellation in linked_constellations: 
                constellation |=  other_constellation
                points[other_point]=first_point

    return list(filter(lambda x: isinstance(x, set), points.values()))

def find_constellation(entry, points):
    if isinstance(points[entry], set):
        return points[entry], entry
    return find_constellation(points[entry], points)

def assimilate(point, known_point, points, links):
    entry, idx_pt = find_constellation(known_point, points)
    entry.add(point)
    points[point] = idx_pt
    if entry not in links.values():
                    links.update({idx_pt: entry})
    return points, links

def close_enough(A,B):
    (x1,y1,z1,t1) = A
    (x2,y2,z2,t2) = B
    return abs(x1-x2) + abs(y1-y2) + abs(z1-z2) + abs(t1-t2) <= 3

def main(file):
    with open(file, 'r') as myfile:
        input = myfile.read()
    constellations = find_constellations(input)
    print("No. of constellations: ", len(constellations))

if __name__ == "__main__":
    main(sys.argv[1])
