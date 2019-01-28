import ply.lex as lex
import ply.yacc as yacc
# This is heavily based on Michael Fogelman's solution
# (https://www.michaelfogleman.com/aoc18/#20)
# and only refactored so I understood it better

directions = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0)
    }

# lexer rules
tokens = ['LPAREN', 'RPAREN', 'OR', 'DIR']

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_OR = r'\|'
t_DIR = r'[NESW]+'


# parser rules
def p_pattern(t):
    'pattern : concat'
    t[0] = t[1]


def p_pattern_or(t):
    'pattern : pattern OR concat'
    t[0] = ('or', t[1], t[3])


def p_concat(t):
    'concat : term'
    t[0] = t[1]


def p_concat_term(t):
    'concat : concat term'
    t[0] = ('concat', t[1], t[2])


def p_term(t):
    'term : DIR'
    t[0] = ('dir', t[1])


def p_term_empty(t):
    'term :'
    t[0] = ('dir', '')


def p_term_paren(t):
    'term : LPAREN pattern RPAREN'
    t[0] = t[2]


def parse(text):
    lexer = lex.lex(errorlog=lex.NullLogger())
    parser = yacc.yacc()
    text = text.strip().replace('^', '').replace('$', '')
    return parser.parse(text, lexer=lexer)


def visit(node, doors, visited):
    if node[0] == 'concat':
        visited = visit(node[1], doors, visited)
        visited = visit(node[2], doors, visited)
        return visited
    elif node[0] == 'or':
        path_a = visit(node[1], doors, visited)
        path_b = visit(node[2], doors, visited)
        return list(set(path_a) | set(path_b))
    else:
        for d in node[1]:
            dx, dy = directions[d]
            doors |= set((x, y, x + dx, y + dy) for x, y in visited)
            doors |= set((x + dx, y + dy, x, y) for x, y in visited)
            visited = [(x + dx, y + dy) for x, y in visited]
        return visited


def locate_doors(text):
    parse_tree = parse(text)
    doors = set()
    visit(parse_tree, doors, [(0, 0)])
    return doors


def search(doors):
    distances = {}
    queue = [(0, 0, 0)]
    while queue:
        x, y, d = queue.pop()
        if (x, y) in distances and distances.get((x, y)) <= d:
            continue
        distances[(x, y)] = d
        for dx, dy in directions.values():
            if (x, y, x + dx, y + dy) in doors:
                queue.append((x + dx, y + dy, d + 1))
    return distances


with open("input.txt", 'r') as myfile:
    input = myfile.readline()
doors = locate_doors(input)
distances = search(doors)
print("Part 1: ", max(distances.values()))
print("Part 2: ", sum(x >= 1000 for x in distances.values()))
