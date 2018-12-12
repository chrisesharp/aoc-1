import sys

def main(file):
    input = open(file, "r").read()
    sum = lic2(0, input.split(' '),0)
    print("Sum:", sum[0])
    
def lic(lvl, tokens, accumulator, rest=[]):
    metadata = []
    if tokens:
        num_children = int(tokens[0])
        num_metadata = int(tokens[1])
        rest = tokens[2:]
        if num_children > 0:
            for i in range(num_children):
                accumulator, metadata, rest = lic(lvl+1,rest, accumulator, rest)
        else:
            metadata = []
        for j in range(num_metadata):
            datum = rest[j]
            metadata.append(datum)
            accumulator += int(datum)
        rest = rest[j+1:]
    return accumulator, metadata, rest

def lic2(lvl, tokens, accumulator, rest=[]):
    metadata = []
    tabs = ""
    if tokens:
        num_children = int(tokens[0])
        num_metadata = int(tokens[1])
        rest = tokens[2:]
        children = []
        have_children = False
        if num_children > 0:
            have_children = True
            for i in range(num_children):
                previous_acc = accumulator
                accumulator, metadata, rest = lic2(lvl+1,rest, 0, rest)
                nodeval = accumulator-previous_acc
                accumulator = previous_acc
                children.append(nodeval)
        else:
            metadata = []
        for j in range(num_metadata):
            datum = rest[j]
            metadata.append(datum)
            if have_children:
                if int(datum) <= len(children):
                    accumulator += children[int(datum)-1]
            else:
                accumulator += int(datum)
        rest = rest[j+1:]
    return accumulator, metadata, rest

if __name__ == "__main__":
    main(sys.argv[1])