import sys

def main(filename):
    file = open(filename, "r")
    print(answer(file))
    
def answer(file):
    accumulator = 0
    for line in file: 
        accumulator += int(line)
    return accumulator

if __name__ == "__main__":
    main(sys.argv[1])