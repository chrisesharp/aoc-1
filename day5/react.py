from tail_recursion import tail_recursive, recurse
import re
import sys
import collections

def transform(input):
    letters = list(collections.Counter(input.lower()).keys())
    best_result = ""
    best = 9999999999
    for letter in letters:
        sample = re.sub(letter, '', input, flags=re.IGNORECASE)
        output = react(sample)
        if len(output) < best:
            best = len(output)
            best_result = output
    return best_result

@tail_recursive
def react(input, accumulator=""):
    if not input:
        return accumulator
    if not reactive_pair(input[0], accumulator[-1:]):
        accumulator = accumulator + input[0]
    else:
        accumulator = accumulator[:-1]
    recurse(input[1:], accumulator)

def reactive_pair(a, b):
    return a.lower() == b.lower() and a != b

def main(file):
    input = open(file, "r").readline().strip()
    print("Part 1:")
    print("Units remaining: ", len(react(input)))
    print("Part 2:")
    output = transform(input)
    print("units left: ",len(output))

if __name__ == "__main__":
    main(sys.argv[1])
        