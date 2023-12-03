import math

neighbor_deltas = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

def get_neighbors(grid, row, col):
    result = []
    for nd in neighbor_deltas:
        if ((len(grid) - 1) >= (row + nd[0]) >= 0) and ((len(grid[0]) -1) >= (col + nd[1]) >= 0):
            result.append({"row":row + nd[0], "col":col + nd[1]})
    return result

def get_and_erase(grid, row, col):
    first_digit = last_digit = col
    while first_digit > 0 and grid[row][first_digit - 1].isdigit():
        first_digit -= 1
    while last_digit < len(grid[0]) - 1 and grid[row][last_digit + 1].isdigit():
        last_digit += 1
    result = int(''.join(grid[row][first_digit:last_digit+1]))
    grid[row][first_digit:last_digit+1] = '.' * (last_digit - first_digit + 1)
    return result


# read in the file as a 2D array of chars
grid = []
with open("dec03in.txt") as my_input:
    for line in my_input:
        grid.append([c for c in line.strip()])

tot = tot_gr = 0
# going line by line, look for symbols. 
for r,line in enumerate(grid):
    for c,element in enumerate(line):
        if not element.isdigit() and not element == '.':            
            part_neighbors = []
            # for each symbol, check each of its adjacent cells,
            for neighbor in get_neighbors(grid, r, c):
                # if there is a digit there, parse it as a number (find all the digits)
                # and *replace* the full number in the array with dots
                # then add that to the running total
                if grid[neighbor['row']][neighbor['col']].isdigit():
                    neighbor = get_and_erase(grid, neighbor["row"], neighbor["col"])
                    tot += neighbor
                    part_neighbors.append(neighbor)
            if element == '*' and len(part_neighbors) == 2:
                tot_gr += math.prod(part_neighbors)

print(tot)
print(tot_gr)