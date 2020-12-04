from collections import Counter
import operator
from functools import reduce

def read_input():
    woods = []

    with open("dec03in.txt") as in_file:

        for line in in_file:
            woods.append(list(line.strip()))    

    return woods

def get_path(woods, start_x, start_y, slope_x, slope_y):
    result = []
    curr_x, curr_y = start_x, start_y
    row_len = len(woods[0])
    while curr_y < len(woods):
        result.append(woods[curr_y][curr_x])
        curr_x = (curr_x + slope_x) % row_len
        curr_y += slope_y

    return result

woods = read_input()

# part 1
path = get_path(woods, 0, 0, 3, 1)
c = Counter(path)
print(path)
print(c['#'])

# part 2:
slopes = ((1,1), (3,1), (5,1), (7,1), (1,2))
counts = []
for slope in slopes:
    path = get_path(woods, 0, 0, slope[0], slope[1])
    c = Counter(path)
    counts.append(c['#'])

print(counts)
print(reduce(operator.mul, counts))